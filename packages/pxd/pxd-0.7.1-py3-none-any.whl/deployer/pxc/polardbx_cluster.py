#   Copyright [2013-2021], Alibaba Group Holding Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import concurrent.futures
import json
import logging
import math
import os
import random
import secrets
import string
import time
from concurrent.futures._base import as_completed
from pathlib import Path

import click
import docker
from humanfriendly import parse_size
from retrying import retry

import deployer.core.docker_manager as DockerManager
from deployer._repo import pxd_working_dir
from deployer.config.config import Config
from deployer.constant import constant
from deployer.constant.constant import PXC_ROOT_ACCOUNT, STORAGE_KIND_GMS, STORAGE_KIND_DN, \
    STORAGE_TYPE_GALAXY_LEADER_ONLY, STORAGE_TYPE_GALAXY_PAXOS
from deployer.core.flow import Flow
from deployer.decorator.decorators import pxc_create_task
from deployer.pxc.gms_consts import SERVER_INFO_DATA_ID_FORMAT, STORAGE_INFO_DATA_ID_FORMAT, CONFIG_DATA_ID_FORMAT, \
    QUARANTINE_CONFIG_DATA_ID_FORMAT, PRIVILEGE_INFO_DATA_ID
from deployer.pxc.pxc_user import PxcUser
from deployer.sqlite import dbapi
from deployer.util.file_manager import FileManager
from deployer.util.mysql_manager import MySQLManager
from deployer.util.password_util import PasswordUtil, random_str
from deployer.xdb.xdb import Xdb, retry_if_result_none, XDB_REQUIRED_ROLES, query_container_role, \
    change_leader_container

logger = logging.getLogger(__name__)

CN_DEFAULT_PARAMS = {
    "CONN_POOL_MAX_POOL_SIZE": "500",
    "max_prepared_stmt_count": "500000",
}


def _extract_resources(topology, role):
    cpu_limit = 16
    mem_limit = 4294967296
    logger.info("extract resources for %s" % role)
    if 'resources' not in topology[role]:
        logger.info("no resources in %s" % role)
        return cpu_limit, mem_limit

    logger.info("topology info: %s" % str(topology[role]['resources']))
    if 'cpu_limit' in topology[role]['resources']:
        cpu_limit = topology[role]['resources']['cpu_limit']

    if 'mem_limit' in topology[role]['resources']:
        mem_limit = parse_size(topology[role]['resources']['mem_limit'], binary=True)

    logger.info("cpu: %s, mem: %s" % (str(cpu_limit), str(mem_limit)))
    return cpu_limit, mem_limit


class PolarDBXCluster:

    def __init__(self, pxc_name, cn_replica=0, cn_version=None, dn_replica=0, dn_version=None, cdc_replica=0,
                 cdc_version=None, columnar_replica=0, columnar_version=None, columnar_engine="OSS",
                 leader_only=True, hosts=['127.0.0.1'], mem_limit='4294967296', topology=None):
        self.pxc_name = pxc_name
        self.pxc_status = 'pending'
        self.cn_replica = cn_replica
        self.cn_version = cn_version
        self.dn_replica = dn_replica
        self.dn_version = dn_version
        self.cdc_replica = cdc_replica
        self.cdc_version = cdc_version
        self.columnar_replica = columnar_replica
        self.columnar_version = columnar_version
        self.columnar_engine = columnar_engine
        self.leader_only = leader_only

        self.gms_image = None
        self.cn_image = None
        self.dn_image = None
        self.cdc_image = None

        self.gms = None
        self.dn_list = []
        self.cn_list = []
        self.cdc_list = []
        self.columnar_list = []

        self.root_account = None
        self.root_password = None
        self.mem_limit = mem_limit
        self.hosts = hosts
        self.topology = topology
        self.error = None
        self.password_key = Config.instance().dn_password_key() if Config.instance().dn_password_key() != '' \
            else random_str(16)

        # cpuset and memory related params
        self.cn_cpu_cores = []
        self.cn_cpu_mems = []
        self.dn_cpu_cores_group = []
        self.dn_cpu_mems_group = []
        self.cdc_cpu_cores = []
        self.cdc_cpu_mems = []
        self.columnar_cpu_cores = []
        self.colunmar_cpu_mems = []

        self.dn_engine = 'galaxy'
        self.dn_engine_version = '8.0'
        self.gms_engine = 'galaxy'
        self.gms_engine_version = '8.0'

        self.create_tasks = [
            self._pre_check_create_pxc,
            self._generate_polardbx_topology,
            self._check_docker_engine_version,
            self._pull_polardbx_related_images,
            self._create_gms,
            self._init_gms_schema,
            self._create_root_account,
            self._create_dn,
            self._insert_dn_list_into_gms,
            self._create_cn_containers,
            self._wait_container_running,
            self._create_cdc_containers,
            self._create_columnar_containers,
            self._finish_create_pxc,
        ]

    def create(self):
        """
        Create a PolarDB-X cluster according to input params.
        """
        logger.info("start create")

        with click.progressbar(self.create_tasks, label="Processing",
                               show_eta=False) as progress_bar:
            for create_task in progress_bar:
                result = create_task()
                if result == Flow.FAIL:
                    break
        if result == Flow.FAIL:
            return
        self._printf_pxc_cluster_info()

    @pxc_create_task(task_name='generate topology')
    def _generate_polardbx_topology(self):
        if self.topology is None:
            logger.info("generate topology without yaml")
            self.gms_image = Config.instance().dn_image
            self.cn_image = Config.instance().cn_image
            self.dn_image = Config.instance().dn_image
            self.cdc_image = Config.instance().cdc_image

            if self.cn_replica > 0:
                self.gms = Xdb(self.pxc_name + '-gms', pxc_name=self.pxc_name, xdb_type='gms', version=self.dn_version,
                               leader_only=self.leader_only)

            for i in range(self.cn_replica):
                self.cn_list.append(PolarDBXCN(self.pxc_name, self.cn_version, self.gms))
            for i in range(self.dn_replica):
                xdb = Xdb(self.pxc_name + '-dn-' + str(i), pxc_name=self.pxc_name, xdb_type='dn',
                          version=self.dn_version, leader_only=self.leader_only)
                self.dn_list.append(xdb)
            for i in range(self.cdc_replica):
                self.cdc_list.append(PolarDBXCDC(self.pxc_name, self.cdc_version, self.gms))
        else:
            logger.info("generate topology with yaml")
            topology = self.topology
            self.parse_yaml_topology(topology)
            self.hosts = list(set(self.hosts))

        Config.instance().load_config(run_host=self.hosts[0])

    def parse_yaml_topology(self, topology):
        self.hosts = []
        self.pxc_name = topology['cluster']['name']

        if 'gms' in topology['cluster']:
            self.parse_gms_topology(topology)

        if 'cn' in topology['cluster']:
            self.parse_cn_topology(topology)

        if 'dn' in topology['cluster']:
            self.parse_dn_topology(topology)

        if 'cdc' in topology['cluster']:
            self.parse_cdc_topology(topology)

        if 'columnar' in topology['cluster']:
            self.parse_columnar_topology(topology)

    def parse_cdc_topology(self, topology):
        self.cdc_replica = topology['cluster']['cdc']['replica']
        if 'image' in topology['cluster']['cdc']:
            self.cdc_image = topology['cluster']['cdc']['image']
        else:
            self.cdc_image = Config.instance().cdc_image
        if self.cdc_replica == 0:
            return

        cdc_cpu_limit, cdc_mem_limit = _extract_resources(topology['cluster'], 'cdc')
        for i in range(self.cdc_replica):
            cdc_host = topology['cluster']['cdc']['nodes'][i]['host']
            self.hosts.append(cdc_host)
            cdc = PolarDBXCDC(self.pxc_name, self.cn_version, self.gms,
                              host=cdc_host, cpu_limit=cdc_cpu_limit,
                              mem_limit=cdc_mem_limit)
            self.cdc_list.append(cdc)
            if 'cpusets' in topology['cluster']['cdc']:
                cdc_cpuset = topology['cluster']['cdc']['cpusets'][i]['cpu']
                self.cdc_cpu_cores.append(cdc_cpuset)
                cdc.cpusets = cdc_cpuset
            if 'memsets' in topology['cluster']['cdc']:
                cdc_memset = topology['cluster']['cdc']['memsets'][i]['mem']
                self.cdc_cpu_mems.append(cdc_memset)
                cdc.memsets = cdc_memset

    def parse_columnar_topology(self, topology):
        self.columnar_replica = topology['cluster']['columnar']['replica']
        if 'image' in topology['cluster']['columnar']:
            self.columnar_image = topology['cluster']['columnar']['image']
        else:
            self.columnar_image = Config.instance().cdc_image

        if self.columnar_replica == 0:
            return

        if 'engine' in topology['cluster']['columnar']:
            self.columnar_engine = topology['cluster']['columnar']['engine']

        columnar_cpu_limit, columnar_mem_limit = _extract_resources(topology['cluster'], 'columnar')
        for i in range(self.columnar_replica):
            columnar_host = topology['cluster']['columnar']['nodes'][i]['host']
            self.hosts.append(columnar_host)
            columnar = PolarDBXColumnar(self.pxc_name, self.cn_version, self.gms,
                                        host=columnar_host, cpu_limit=columnar_cpu_limit,
                                        mem_limit=columnar_mem_limit, engine=self.columnar_engine)
            self.columnar_list.append(columnar)
            if 'cpusets' in topology['cluster']['columnar']:
                columnar_cpuset = topology['cluster']['columnar']['cpusets'][i]['cpu']
                self.columnar_cpu_cores.append(columnar_cpuset)
                columnar.cpusets = columnar_cpuset
            if 'memsets' in topology['cluster']['columnar']:
                columnar_memset = topology['cluster']['columnar']['memsets'][i]['mem']
                self.columnar_cpu_mems.append(columnar_memset)
                columnar.memsets = columnar_memset

    def parse_dn_topology(self, topology):
        if 'image' in topology['cluster']['dn']:
            self.dn_image = topology['cluster']['dn']['image']
        else:
            self.dn_image = Config.instance().dn_image

        self.dn_replica = topology['cluster']['dn']['replica']
        if 'engine' in topology['cluster']['dn']:
            self.dn_engine = topology['cluster']['dn']['engine']
        if 'engine_version' in topology['cluster']['dn']:
            self.dn_engine_version = topology['cluster']['dn']['engine_version']

        dn_cpu_limit, dn_mem_limit = _extract_resources(topology['cluster'], 'dn')
        for i in range(self.dn_replica):
            dn_host = topology['cluster']['dn']['nodes'][i]['host_group']
            self.hosts.extend(dn_host)
            xdb = Xdb(self.pxc_name + '-dn-' + str(i), pxc_name=self.pxc_name, xdb_type='dn',
                      version=self.dn_version, engine_image=self.dn_image,
                      hosts=dn_host, leader_only=(len(dn_host) == 1),
                      cpu_limit=dn_cpu_limit, mem_limit=dn_mem_limit, engine_type=self.dn_engine,
                      engine_version=self.dn_engine_version)
            self.dn_list.append(xdb)
            if 'cpusets' in topology['cluster']['dn']:
                dn_cpusets = topology['cluster']['dn']['cpusets'][i]['cpu_group']
                xdb.cpusets = dn_cpusets
            if 'memsets' in topology['cluster']['dn']:
                dn_memsets = topology['cluster']['dn']['memsets'][i]['mem_group']
                xdb.memsets = dn_memsets

    def parse_cn_topology(self, topology):
        if 'image' in topology['cluster']['cn']:
            self.cn_image = topology['cluster']['cn']['image']
        else:
            self.cn_image = Config.instance().cn_image

        self.cn_replica = topology['cluster']['cn']['replica']
        cn_cpu_limit, cn_mem_limit = _extract_resources(topology['cluster'], 'cn')
        for i in range(self.cn_replica):
            cn_host = topology['cluster']['cn']['nodes'][i]['host']
            self.hosts.append(cn_host)
            cn = PolarDBXCN(self.pxc_name, self.cn_version, self.gms,
                            host=cn_host,
                            cpu_limit=cn_cpu_limit,
                            mem_limit=cn_mem_limit)
            self.cn_list.append(cn)
            if 'cpusets' in topology['cluster']['cn']:
                cn_cpuset = topology['cluster']['cn']['cpusets'][i]['cpu']
                self.cn_cpu_cores.append(cn_cpuset)
                cn.cpusets = cn_cpuset
            if 'memsets' in topology['cluster']['cn']:
                cn_memset = topology['cluster']['cn']['memsets'][i]['mem']
                self.cn_cpu_mems.append(cn_memset)
                cn.memsets = cn_memset

    def parse_gms_topology(self, topology):
        if 'image' in topology['cluster']['gms']:
            self.gms_image = topology['cluster']['gms']['image']
        else:
            self.gms_image = Config.instance().dn_image

        if 'engine' in topology['cluster']['gms']:
            self.gms_engine = topology['cluster']['gms']['engine']
        if 'engine_version' in topology['cluster']['gms']:
            self.gms_engine_version = topology['cluster']['gms']['engine_version']

        gms_hosts = topology['cluster']['gms']['host_group']
        self.hosts.extend(gms_hosts)
        self.leader_only = len(gms_hosts) == 1
        gms_cpu_limit, gms_mem_limit = _extract_resources(topology['cluster'], 'gms')
        self.gms = Xdb(self.pxc_name + '-gms', pxc_name=self.pxc_name, xdb_type='gms', version=self.dn_version,
                       engine_image=self.gms_image, hosts=gms_hosts, leader_only=self.leader_only,
                       cpu_limit=gms_cpu_limit, mem_limit=gms_mem_limit, engine_type=self.gms_engine,
                       engine_version=self.gms_engine_version
                       )

    @pxc_create_task(task_name="check docker engine version")
    def _check_docker_engine_version(self):
        for host in self.hosts:
            try:
                logger.info("check %s host docker engine" % host)
                client = DockerManager.get_client(host)
                client.info()
            except Exception as ex:
                logger.error("check docker engine failed", ex)
                click.echo("\n")
                click.echo(
                    click.style("Error: Connect to remote docker failed. Please check docker version of host: %s. "
                                "Make sure docker version >= 18.09" % host, fg='red'))
                return Flow.FAIL

    @pxc_create_task(task_name="pull images")
    def _pull_polardbx_related_images(self):
        if not Config.pull_latest_images():
            logger.info("Skip pull latest images")
            return

        max_workers = min(len(self.hosts), 8)
        images_list = [self.dn_image,
                       Config.instance().dn_tool_image]
        if self.cn_replica > 0:
            images_list.append(self.cn_image)
            images_list.append(Config.instance().cn_tool_image)
        if self.cdc_replica > 0:
            images_list.append(self.cdc_image)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = [executor.submit(_pull_images, host, images_list) for host in self.hosts]
            for f in as_completed(results):
                logger.info(f.result())

    @pxc_create_task(task_name='pre check')
    def _pre_check_create_pxc(self):
        # check same cluster existing
        pxc = dbapi.get_pxc_by_name(pxc_name=self.pxc_name)
        if len(pxc) > 0:
            click.echo("\n")
            click.echo(click.style("Error: %s pxc cluster is already existing, please use `pxd delete %s` to remove it "
                                   "first." % (self.pxc_name, self.pxc_name), fg='red'))
            return Flow.FAIL
        self.pxc_status = 'creating'

    @pxc_create_task(task_name='create gms node', task_type="enterprise")
    def _create_gms(self):
        if self.gms is not None:
            self.gms.create()

    @pxc_create_task(task_name='create dn')
    def _create_dn(self):
        def _create_dn(xdb):
            xdb.create()

        max_workers = min(len(self.dn_list), 8)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = []
            for xdb in self.dn_list:
                time.sleep(5)
                results.append(executor.submit(_create_dn, xdb))

            for f in as_completed(results):
                logger.info(f.result())

    @pxc_create_task(task_name='create gms db and tables', task_type="enterprise")
    def _init_gms_schema(self):
        if self.gms is None:
            return Flow.SUCCESS
        self._create_metadb_and_tables()
        self._insert_metadata_to_gms()

    def _create_metadb_and_tables(self):
        cur_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute()
        statement = ''
        # TODO: refine sql file execute
        for line in open(f'{cur_dir}/resources/sql/gms_init.sql'):
            if line == '' or line.startswith('#'):
                continue
            statement += line
        MySQLManager.execute_update(self.gms, [statement], db='')

    def _insert_metadata_to_gms(self):
        sql_list = ["insert ignore into `schema_change`(`table_name`, `version`) values('user_priv', 1);"]
        sql_list.append(self._generate_xdb_storage_info_sql([self.gms], STORAGE_KIND_GMS))
        sql_list.append(
            f"INSERT IGNORE INTO `quarantine_config` VALUES (NULL, NOW(), NOW(), '{self.pxc_name}', 'default', "
            f"NULL, NULL, '0.0.0.0/0');")

        for dataId in [SERVER_INFO_DATA_ID_FORMAT, STORAGE_INFO_DATA_ID_FORMAT, CONFIG_DATA_ID_FORMAT,
                       QUARANTINE_CONFIG_DATA_ID_FORMAT]:
            sql = "INSERT IGNORE INTO config_listener (id, gmt_created, gmt_modified, " \
                  "data_id, status, op_version, extras) " \
                  "VALUES (NULL, NOW(), NOW(), '%s', 0, 0, NULL);" % (dataId % self.pxc_name)
            sql_list.append(sql)
        sql_list.append("INSERT IGNORE INTO config_listener (id, gmt_created, gmt_modified, " \
                        "data_id, status, op_version, extras) " \
                        "VALUES (NULL, NOW(), NOW(), '%s', 0, 0, NULL);" % PRIVILEGE_INFO_DATA_ID)

        sql_list.append(f"insert into inst_config (inst_id, param_key,param_val) "
                        f"values ('{self.pxc_name}','CONN_POOL_XPROTO_META_DB_PORT',"
                        f"'0')")

        cdc_startup_mode = '1' if self.cdc_replica > 0 else '0'
        sql_list.append(f"insert into inst_config (inst_id, param_key,param_val) "
                        f"values ('{self.pxc_name}','CDC_STARTUP_MODE',"
                        f"'{cdc_startup_mode}')")

        for (key, value) in CN_DEFAULT_PARAMS.items():
            sql_list.append(f"replace into inst_config (inst_id, param_key,param_val) "
                            f"values ('{self.pxc_name}','{key}',"
                            f"'{value}')")
        MySQLManager.execute_update(self.gms, sql_list)

    @pxc_create_task(task_name='create PolarDB-X root account', task_type="enterprise")
    def _create_root_account(self):
        if self.gms is None:
            return Flow.SUCCESS

        root_password = ''.join(secrets.choice(string.ascii_letters) for i in range(8))
        self.root_account = PXC_ROOT_ACCOUNT
        self.root_password = root_password
        pxc_user = PxcUser(self.root_account, self.root_password)
        sql_list = [self._generate_pxc_account_sql(pxc_user),
                    self._generate_notify_data_id_change_sql(PRIVILEGE_INFO_DATA_ID)]
        MySQLManager.execute_update(self.gms, sql_list)
        logger.info("account: %s, password: %s", self.root_account, self.root_password)

    def _generate_pxc_account_sql(self, pxc_user):
        return f"INSERT IGNORE INTO user_priv (id, gmt_created, gmt_modified, user_name, host, password, select_priv, " \
               f"insert_priv, update_priv, delete_priv, create_priv, drop_priv, grant_priv, index_priv, alter_priv, " \
               f"show_view_priv, create_view_priv, create_user_priv, meta_db_priv) " \
               f"VALUES (NULL, now(), now(), '{pxc_user.user_name}', '{pxc_user.host}', '{pxc_user.enc_password}', " \
               f"'{pxc_user.select_priv}', '{pxc_user.insert_priv}', '{pxc_user.update_priv}', '{pxc_user.delete_priv}', " \
               f"'{pxc_user.create_priv}', '{pxc_user.drop_priv}', '{pxc_user.grant_priv}', '{pxc_user.index_priv}', " \
               f"'{pxc_user.alter_priv}', '{pxc_user.show_view_priv}', '{pxc_user.create_view_priv}', '{pxc_user.create_user_priv}', " \
               f"'{pxc_user.meta_db_priv}')"

    def _generate_notify_data_id_change_sql(self, data_id):
        return f"UPDATE config_listener SET op_version = op_version + 1 WHERE data_id = '{data_id}'"

    def _generate_xdb_storage_info_sql(self, xdb_list, storage_kind):
        if not xdb_list:
            return ''
        insert_values = []
        for xdb in xdb_list:
            storage_type = xdb.storage_type()
            is_vip = '0'
            # is_vip = '1' if storage_kind == STORAGE_KIND_GMS else '0'
            insert_values.append(
                f"(NULL, NOW(), NOW(), '{self.pxc_name}', '{xdb.name}', '{xdb.name}',"
                f" '{xdb.leader_node.container_ip if xdb.leader_node.host == '127.0.0.1' else xdb.leader_node.host}', " \
                f"{xdb.leader_node.mysql_port}, {xdb.leader_node.polarx_port}, '{xdb.user_name}', "
                f"'{PasswordUtil().encrypt(self.password_key, xdb.password)}', " \
                f"{storage_type}, {storage_kind}, 0, NULL, NULL, NULL, 10000, 4, {8 << 30}, {is_vip}, '')")
        sql = "INSERT IGNORE INTO storage_info (id, gmt_created, gmt_modified, inst_id, storage_inst_id, " \
              "storage_master_inst_id,ip, port, xport, user, passwd_enc, storage_type, inst_kind, status, " \
              "region_id, azone_id, idc_id, max_conn, cpu_core, mem_size, is_vip, extras) VALUES " + " , ".join(
            insert_values) + ";"
        return sql

    @pxc_create_task(task_name="register dn to gms", task_type="enterprise")
    def _insert_dn_list_into_gms(self):
        if self.gms is None:
            return Flow.SUCCESS

        sql_list = [self._generate_xdb_storage_info_sql(self.dn_list, STORAGE_KIND_DN),
                    self._generate_notify_data_id_change_sql(STORAGE_INFO_DATA_ID_FORMAT % self.pxc_name)]
        MySQLManager.execute_update(self.gms, sql_list)

    @pxc_create_task(task_name='create cn', task_type="enterprise")
    def _create_cn_containers(self):
        for cn in self.cn_list:
            self._start_cn_container(cn)

    @retry(stop_max_attempt_number=5, wait_fixed=2000, retry_on_result=retry_if_result_none)
    def _start_cn_container(self, cn):
        try:
            client = DockerManager.get_client(cn.host)
            ports = cn.generate_ports()
            export_ports = cn.generate_export_ports()
            volumes = cn.generate_volumes()
            if len(self.columnar_list) > 0:
                nfs_dir = f'{pxd_working_dir}/nfs/'
                volumes[nfs_dir] = {"bind": "/home/admin/polardbx-external-disk", "mode": "rw"}
            envs = cn.generate_envs(self.password_key, self.dn_engine)
            entrypoint = '/home/admin/entrypoint.sh 20'
            if self.dn_engine == 'xcluster':
                entrypoint = 'bash -c "/home/admin/basic_init/init.sh /home/admin/app.sh"'

            if Config.host_network_support():
                for log in client.containers.run(
                        Config.instance().cn_tool_image,
                        environment=envs, command="/init",
                        network_mode='host',
                        volumes=volumes,
                        privileged=True,
                        remove=not Config.debug_mode_enabled(),
                        stream=True,
                        name=self.pxc_name + '-cn-init-' + random_str(4)):
                    logger.info("init container logs: %s" % log)

                container = client.containers.run(self.cn_image,
                                                  detach=True,
                                                  mem_limit=cn.mem_limit,
                                                  volumes=volumes,
                                                  privileged=True,
                                                  entrypoint=entrypoint,
                                                  environment=envs,
                                                  name=cn.name,
                                                  network_mode='host',
                                                  cpuset_cpus=cn.cpusets,
                                                  cpuset_mems=cn.memsets
                                                  )
            else:
                for log in client.containers.run(
                        Config.instance().cn_tool_image,
                        environment=envs, command="/init",
                        volumes=volumes,
                        privileged=True,
                        remove=not Config.debug_mode_enabled(),
                        stream=True,
                        name=self.pxc_name + '-cn-init-' + random_str(4)):
                    logger.info("init container logs: %s" % log)

                container = client.containers.run(self.cn_image,
                                                  detach=True,
                                                  privileged=True,
                                                  mem_limit=cn.mem_limit,
                                                  volumes=volumes,
                                                  entrypoint='/home/admin/entrypoint.sh 20',
                                                  environment=envs,
                                                  name=cn.name,
                                                  ports=export_ports,
                                                  cpuset_cpus=cn.cpusets,
                                                  cpuset_mems=cn.memsets
                                                  )
            cn.container_id = container.short_id
            dbapi.update_container(self.pxc_name, container,
                                   host=cn.host, role='cn-engine',
                                   volumes=json.dumps(volumes), ports=json.dumps(ports), envs=json.dumps(envs))
            return True
        except Exception as ex:
            logger.info("failed to create cn container, %s" % str(ex))
            return None

    @pxc_create_task(task_name='create cdc containers', task_type="enterprise")
    def _create_cdc_containers(self):
        if len(self.cdc_list) == 0:
            logger.info("cdc list is empty, does not need to create")
            return

        for cdc in self.cdc_list:
            client = DockerManager.get_client(cdc.host)
            ports = cdc.generate_ports()
            volumes = cdc.generate_volumes()
            envs = cdc.generate_envs(self.cn_list, self.root_account, self.root_password, self.password_key)

            container = client.containers.run(self.cdc_image,
                                              command="",
                                              detach=True,
                                              mem_limit=cdc.mem_limit,
                                              entrypoint="",
                                              privileged=True,
                                              environment=envs,
                                              volumes=volumes,
                                              name=cdc.name,
                                              network_mode='host' if Config.instance().host_network_support() else 'bridge',
                                              cpuset_cpus=cdc.cpusets,
                                              cpuset_mems=cdc.memsets
                                              )

            dbapi.update_container(self.pxc_name, container,
                                   host=cdc.host, role='cdc-engine',
                                   volumes=json.dumps(volumes), ports=json.dumps(ports), envs=json.dumps(envs))

    @pxc_create_task(task_name='create columnar containers', task_type="enterprise")
    def _create_columnar_containers(self):
        if len(self.columnar_list) == 0:
            logger.info("columnar list is empty, does not need to create")
            return

        for columnar in self.columnar_list:
            client = DockerManager.get_client(columnar.host)
            ports = columnar.generate_ports()
            volumes = columnar.generate_volumes()

            envs = columnar.generate_envs(self.cn_list, self.root_account, self.root_password, self.password_key)

            container = client.containers.run(self.columnar_image,
                                              command="",
                                              detach=True,
                                              mem_limit=columnar.mem_limit,
                                              entrypoint="",
                                              privileged=True,
                                              environment=envs,
                                              volumes=volumes,
                                              name=columnar.name,
                                              network_mode='host' if Config.instance().host_network_support() else 'bridge',
                                              cpuset_cpus=columnar.cpusets,
                                              cpuset_mems=columnar.memsets
                                              )

            dbapi.update_container(self.pxc_name, container,
                                   host=columnar.host, role='columnar-engine',
                                   volumes=json.dumps(volumes), ports=json.dumps(ports), envs=json.dumps(envs))

    @retry(stop_max_attempt_number=20, wait_fixed=5000, retry_on_result=retry_if_result_none)
    def _wait_pxc_ready(self):
        for cn in self.cn_list:
            try:
                logger.info("try probe cn: %s" % str(cn))
                MySQLManager.execute_cn_sql(cn, self.root_password, 'show storage')
                return True
            except Exception as e:
                logger.info("failed to check pxc status, cn: %s,  ex: %s" % (str(cn), str(e)))
                return None

        return True

    @pxc_create_task(task_name='create file storage', task_type="enterprise")
    def _create_file_storage(self):
        if len(self.columnar_list) < 1:
            return Flow.SUCCESS

        self._wait_pxc_ready()

        if self.columnar_engine == 'oss':
            pass
        elif self.columnar_engine == 'local_storage':
            pass
        elif self.columnar_engine == 'external_storage':
            pass
        else:
            logger.error("Specified columnar engine is not supported")
            return Flow.FAIL

    @pxc_create_task(task_name='wait PolarDB-X ready')
    def _finish_create_pxc(self):
        try:
            self._wait_pxc_ready()
        except Exception as ex:
            logger.warn("pxc status check failed, but not block. %s" % str(ex))
        self.pxc_status = 'running'

    def _printf_pxc_cluster_info(self):
        click.echo("\n")
        click.echo("PolarDB-X cluster create successfully, you can try it out now.")
        click.echo(click.style("Connect PolarDB-X using the following command:"))
        click.echo()
        if self.gms is None:
            # PolarDB-X Standard
            click.echo('    ' + click.style("mysql -h%s -P%d -u%s -p%s" % (self.dn_list[0].leader_node.host,
                                                                           self.dn_list[0].leader_node.mysql_port,
                                                                           self.dn_list[0].user_name,
                                                                           self.dn_list[0].password)))
        else:
            # PolarDB-X Enterprise
            for cn in self.cn_list:
                click.echo('    ' + click.style("mysql -h%s -P%d -u%s -p%s" % (cn.host, cn.mysql_port, 'polardbx_root',
                                                                               self.root_password)))

    @pxc_create_task(task_name='wait cn ready', task_type="enterprise")
    @retry(stop_max_attempt_number=10, wait_fixed=5000, retry_on_result=retry_if_result_none)
    def _wait_container_running(self):
        for cn in self.cn_list:
            client = DockerManager.get_client(cn.host)
            container = client.containers.get(cn.container_id)
            if container.status != 'running':
                return None

            cn.container_ip = container.attrs['NetworkSettings']['IPAddress']

        return "True"

    @staticmethod
    def delete(pxc_name):
        """
        Delete specific polardb-x cluster
        :param pxc_name: cluster name
        :return:
        """
        click.echo("Prepare to delete PolarDB-X cluster: %s" % pxc_name)
        containers = []
        cn_cdc_containers = dbapi.list_containers_by_pxc(pxc_name)
        if cn_cdc_containers is not None:
            containers.extend(cn_cdc_containers)

        xdbs = dbapi.list_xdbs_by_pxc(pxc_name)
        xdb_names = []
        for xdb in xdbs:
            xdb_names.append(f"'{xdb['xdb_name']}'")

        xdb_containers = dbapi.list_xdb_containers_by_names(xdb_names)
        if xdb_containers is not None:
            containers.extend(xdb_containers)

        local_volumes = []
        for container in containers:
            container_name = container['container_name']
            container_id = container['container_id']
            container_host = container['host']
            click.echo('stop and remove container: %s, id: %s at %s' % (container_name, container_id, container_host))
            volumes = container['local_volumes']
            if volumes:
                local_volumes.append((container_host, volumes))
            stop_and_remove_container(container_host, container_id)

        for host, volume in local_volumes:
            rm_volumes_if_needed(host, json.loads(volume))

        dbapi.delete_pxc_related_records(pxc_name)

    @staticmethod
    def check_dn_leader(pxc_name, repair=False):
        xdbs = dbapi.list_xdbs_by_pxc(pxc_name)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = []
            for xdb in xdbs:
                results.append(executor.submit(check_and_repair_dn, xdb, repair))

            for f in as_completed(results):
                logger.info(f.result())

    @staticmethod
    def check_cn_alive(pxc_name, repair=False):
        cn_containers = dbapi.list_cn_containers_by_pxc(pxc_name)

        for container in cn_containers:
            container_name = container['container_name']
            container_id = container['container_id']
            container_host = container['host']
            values = container_name.split("-")
            server_port = values[len(values) - 1]
            logger.info("prepare check cn: %s, host: %s" % (container_name, container_host))
            cmd = "mysql -h127.1 -P%s -upolardbx_root -e 'select 1'" % str(server_port)
            result = exec_cmd_for_cn(host=container_host, container_name=container_name,
                                     container_id=container_id, cmd=cmd)
            if not result:
                click.echo("cn: %s host: %s is not alive" % (container_name, container_host))
                if repair:
                    restart_result = exec_cmd_for_cn(host=container_host, container_name=container_name,
                                                     container_id=container_id,
                                                     cmd="su admin -c \"sh /home/admin/drds-server/bin/restart.sh\"")
                    if not restart_result:
                        click.echo("restart cn fail, container: %s, host: %s" % (container_name, container_host))
                    else:
                        click.echo("restart cn success, container: %s, host: %s" % (container_name, container_host))
            else:
                click.echo("cn: %s host: %s is OK!" % (container_name, container_host))

    @staticmethod
    def upgrade(pxc_name, type, image):
        if type in ('cn', 'cdc', 'columnar'):
            containers = dbapi.list_containers_by_pxc_and_type(pxc_name, type)
            for container in containers:
                restart_container_with_new_image(container, image)
        elif type in ('gms', 'dn'):
            xdbs = dbapi.list_xdbs_by_type(pxc_name, type)
            for xdb in xdbs:
                click.echo("prepare upgrade xdb: %s" % xdb['xdb_name'])
                containers = dbapi.list_containers_by_pxc_and_type(xdb['xdb_name'], type)
                containers = reorder_xdb_containers_for_restart(xdb['xdb_name'], containers)
                if containers is None:
                    return
                for container in containers:
                    click.echo(container['container_name'])
                    restart_container_with_new_image(container, image)
        else:
            click.echo("unknown component type: %s" % type)


class PolarDBXCN:
    existing_ip_pots = {}

    def __init__(self, pxc_name, version, gms, host='127.0.0.1', cpu_limit=1, mem_limit='2147483648'):
        self.version = version
        self.pxc_name = pxc_name
        self.name = pxc_name + '-cn-' + random_str(4)
        self.gms = gms
        self.host = host
        self.cpu_limit = cpu_limit
        self.mem_limit = mem_limit
        self.container_id = None
        self.container_ip = None
        self.mysql_port = None
        self.mgr_port = None
        self.mpp_port = None
        self.htap_port = None
        self.log_port = None
        self.metrics_port = None
        self.jmx_port = None
        self.debug_port = None
        self.cpusets = None
        self.memsets = None

    def generate_ports(self):
        self.mysql_port = int((random.randint(49152, 64535) / 8) * 8)
        ip_ports = "%s:%s" % (self.host, str(self.mysql_port))
        while ip_ports in self.existing_ip_pots:
            logger.info("cn ip port conflict, ip_ports: %s" % ip_ports)
            self.mysql_port = int((random.randint(49152, 64535) / 8) * 8)
            ip_ports = "%s:%s" % (self.host, str(self.mysql_port))
        self.existing_ip_pots[ip_ports] = 1
        self.name += '-%s' % str(self.mysql_port)
        self.mgr_port = self.mysql_port + 1
        self.mpp_port = self.mysql_port + 2
        self.htap_port = self.mysql_port + 3
        self.log_port = self.mysql_port + 4
        self.metrics_port = self.mysql_port + 5
        self.jmx_port = self.mysql_port + 6
        self.debug_port = self.mysql_port + 7
        ports = {str(self.mysql_port) + '/tcp': self.mysql_port,
                 str(self.mgr_port) + '/tcp': self.mgr_port,
                 str(self.mpp_port) + '/tcp': self.mpp_port,
                 str(self.htap_port) + '/tcp': self.htap_port,
                 str(self.log_port) + '/tcp': self.log_port,
                 str(self.metrics_port) + '/tcp': self.metrics_port,
                 str(self.jmx_port) + '/tcp': self.jmx_port,
                 str(self.debug_port) + '/tcp': self.debug_port}
        return ports

    def generate_export_ports(self):
        return {
            str(self.mysql_port) + '/tcp': self.mysql_port
        }

    def generate_volumes(self):
        return {
            "/etc/localtime": {"bind": "/etc/localtime", "mode": "ro"},
            "/usr/share/zoneinfo": {"bind": "/usr/share/zoneinfo", "mode": "ro"}
        }

    def generate_envs(self, password_key, engine_type="galaxy"):
        leader = self.gms.leader_node
        leader_ip = leader.host if Config.instance().host_network_support() else leader.container_ip
        metadb_conn = "mysql -h%s -P%d -u%s -p%s -D%s" % (leader_ip, leader.mysql_port, self.gms.user_name,
                                                          self.gms.password, 'polardbx_meta_db')

        galayxXProtocol = "0"
        if engine_type == constant.GALAXY_ENGINE:
            galayxXProtocol = Config.rpc_protocol_version()

        pod_ip = self.host if Config.instance().host_network_support() else str(self.container_ip)
        envs = ['POD_ID=' + str(self.name),
                'HOST_IP=' + str(self.host),
                'NODE_NAME=' + str(self.host),
                'switchCloud=aliyun',
                'metaDbAddr=%s:%d' % (
                    leader_ip, leader.mysql_port),
                'metaDbName=polardbx_meta_db',
                'metaDbUser=' + self.gms.user_name,
                'metaDbPasswd=' + PasswordUtil().encrypt(password_key, self.gms.password),
                'metaDbXprotoPort=0',
                'storageDbXprotoPort=0',
                'galaxyXProtocol=' + galayxXProtocol,
                'metaDbConn=' + metadb_conn,
                'instanceId=' + self.pxc_name,
                'instanceType=0',
                'serverPort=' + str(self.mysql_port),
                'mgrPort=' + str(self.mgr_port),
                'mgrPort=' + str(self.mgr_port),
                'mppPort=' + str(self.mpp_port),
                'rpcPort=' + str(self.mpp_port),
                'htapPort=' + str(self.htap_port),
                'logPort=' + str(self.log_port),
                'ins_id=dummy',
                'polarx_dummy_log_port=' + str(self.log_port),
                'polarx_dummy_ssh_port=-1',
                'cpuCore=' + str(self.cpu_limit),
                'memSize=' + str(self.mem_limit),
                'cpu_cores=' + str(self.cpu_limit),
                'memory=' + str(self.mem_limit),
                'TDDL_OPTS=-Dpod.id=$(POD_ID) -DinstanceVersion=8.0.3',
                'dnPasswordKey=' + password_key,
                'LANG=en_US.utf8',
                'LC_ALL=en_US.utf8',
                ]
        if pod_ip != "None":
            envs.append("POD_IP=" + pod_ip)

        return envs


class PolarDBXCDC:

    def __init__(self, pxc_name, version, gms, host='127.0.0.1', cpu_limit=1, mem_limit='2147483648'):
        self.pxc_name = pxc_name
        self.name = pxc_name + '-cdc-' + random_str(4)
        self.daemon_port = random.randint(3000, 3300)
        self.version = version
        self.gms = gms
        self.host = host
        self.container_id = None
        self.container_ip = None
        self.cpu_limit = cpu_limit
        self.mem_limit = mem_limit

        self.cpusets = None
        self.memsets = None

    def generate_ports(self):
        return {'3300/tcp': 3300}

    def generate_volumes(self):
        return {
            "/etc/localtime": {"bind": "/etc/localtime", "mode": "ro"},
            "/usr/share/zoneinfo": {"bind": "/usr/share/zoneinfo", "mode": "ro"}
        }

    def generate_envs(self, cn_list, pxc_root_account, pxc_root_password, password_key):
        leader = self.gms.leader_node
        leader_ip = leader.host if Config.instance().host_network_support() else leader.container_ip
        gms_jdbc_url = "jdbc:mysql://%s:%s/polardbx_meta_db?useSSL=false" % (leader_ip, leader.mysql_port)
        cn = cn_list[0]
        cn_ip = cn.host if Config.instance().host_network_support() else cn.container_ip
        polarx_jdbc_url = "jdbc:mysql://%s:%s/__cdc__?useSSL=false" % (cn_ip, cn.mysql_port)

        common_ports = {
            "ssh_port": "2200",
            "access_port": "%s" % self.daemon_port,
            "link": "0",
            "cdc1_port": "6061",
            "cdc2_port": "6062",
            "cdc3_port": "6063",
            "cdc4_port": "6064",
            "cdc5_port": "6065",
            "cdc6_port": "6066"
        }

        envs = ['switchCloud=aliyun',
                'topology_node_minsize=1',
                'cluster_id=' + self.pxc_name,
                'ins_id=' + self.name,
                'daemonPort=' + str(self.daemon_port),
                'daemon_port=' + str(self.daemon_port),
                'port={"' + self.name + '":{"ssh_port":[2200],"access_port":[3300],"link":[0],"cdc1_port":[6061],"cdc2_port":[6062],"cdc3_port":[6063],"cdc4_port":[6064],"cdc5_port":[6065],"cdc6_port":[6066]}}',
                'common_ports=' + json.dumps(common_ports),
                'cpu_cores=' + str(self.cpu_limit),
                'cpuCore=' + str(self.cpu_limit),
                'mem_size=' + str(math.floor(int(self.mem_limit) / 1024 / 1024)),
                'disk_size=10240',
                'disk_quota=10240',
                'metaDb_url=' + gms_jdbc_url,
                'metaDb_username=' + self.gms.user_name,
                'metaDb_password=' + self.gms.password,
                'polarx_url=' + polarx_jdbc_url,
                'polarx_username=' + pxc_root_account,
                'polarx_password=' + pxc_root_password,
                'dnPasswordKey=' + password_key,
                'LANG=en_US.utf8',
                'LC_ALL=en_US.utf8',
                ]

        if self.host != '127.0.0.1':
            envs.append("ins_ip=" + self.host)

        return envs


class PolarDBXColumnar:

    def __init__(self, pxc_name, version, gms, host='127.0.0.1', cpu_limit=1, mem_limit='2147483648',
                 engine="OSS"):
        self.pxc_name = pxc_name
        self.name = pxc_name + '-columnar-' + random_str(4)
        self.version = version
        self.gms = gms
        self.host = host
        self.container_id = None
        self.container_ip = None
        self.cpu_limit = cpu_limit
        self.mem_limit = mem_limit
        self.engine = engine

        self.cpusets = None
        self.memsets = None

    def generate_ports(self):
        return {
            '3007/tcp': 3007,
            '3070/tcp': 3070}

    def generate_volumes(self):
        columnar_log_dir = f'{pxd_working_dir}/data/polarx-log/{self.name}'
        nfs_dir = f'{pxd_working_dir}/nfs/'
        volumes = {
            columnar_log_dir: {"bind": "/home/admin/polardbx-columnar/logs", "mode": "rw"},
            nfs_dir: {"bind": "/home/admin/polardbx-external-disk", "mode": "rw"}
        }
        self.create_volume_dirs_if_needed(volumes)
        volumes.update({
            "/etc/localtime": {"bind": "/etc/localtime", "mode": "ro"},
            "/usr/share/zoneinfo": {"bind": "/usr/share/zoneinfo", "mode": "ro"}
        })
        return volumes

    def create_volume_dirs_if_needed(self, volumes):
        logger.info("try to mkdirs, host: %s, dirs: %s" % (self.host, volumes.keys()))
        FileManager.mkdirs(self.host, volumes.keys())

    def generate_envs(self, cn_list, pxc_root_account, pxc_root_password, password_key):
        leader = self.gms.leader_node
        leader_ip = leader.host if Config.instance().host_network_support() else leader.container_ip
        gms_jdbc_url = "jdbc:mysql://%s:%s/polardbx_meta_db?useSSL=false" % (leader_ip, leader.mysql_port)
        cn = cn_list[0]
        cn_ip = cn.host if Config.instance().host_network_support() else cn.container_ip
        polarx_jdbc_url = "jdbc:mysql://%s:%s/__cdc__?useSSL=false" % (cn_ip, cn.mysql_port)

        envs = ['switchCloud=aliyun',
                'cluster_id=' + self.pxc_name + 'columnar',
                'ins_id=' + self.name,
                'port={"' + self.name + '":{"ssh_port":[2200],"access_port":[3300],"link":[0],"cdc1_port":[6061],"cdc2_port":[6062],"cdc3_port":[6063],"cdc4_port":[6064],"cdc5_port":[6065],"cdc6_port":[6066]}}',
                'cpu_cores=' + str(self.cpu_limit),
                'cpuCore=' + str(self.cpu_limit),
                'mem_size=' + str(math.floor(int(self.mem_limit) / 1024 / 1024)),
                'disk_size=10240',
                'disk_quota=10240',
                'metaDb_url=' + gms_jdbc_url,
                'metaDbAddr=%s:%s' % (leader_ip, leader.mysql_port),
                'metaDbName=polardbx_meta_db',
                'metaDbUser=' + self.gms.user_name,
                'metaDbPasswd=' + PasswordUtil().encrypt(password_key, self.gms.password),
                'metaDb_username=' + self.gms.user_name,
                'metaDb_password=' + self.gms.password,
                'metaDbXprotoPort=' + str(leader.polarx_port),
                'storageDbXprotoPort=0',
                'polarx_url=' + polarx_jdbc_url,
                'polarx_username=' + pxc_root_account,
                'polarx_password=' + pxc_root_password,
                'dnPasswordKey=' + password_key,
                'LANG=en_US.utf8',
                'LC_ALL=en_US.utf8',
                'columnar_ports={"columnar_port": "3070"}',
                'cluster_type=COLUMNAR',
                'daemon_port=3007',
                'columnarPort=3070',
                'columnar_engine=' + self.engine
                ]

        if self.host != '127.0.0.1':
            envs.append("ins_ip=" + self.host)

        return envs


def stop_and_remove_container(host, container_id):
    client = DockerManager.get_client(host)
    try:
        container = client.containers.get(container_id)
        if container.status == 'running':
            container.stop()
        # remove docker container and its volumes
        container.remove(v=True, force=True)
    except docker.errors.NotFound:
        click.echo('container: %s is not existing at %s.' % (container_id, host))


def restart_container_with_new_image(container: dict, new_image: str):
    container_name = container['container_name']
    container_id = container['container_id']
    envs = json.loads(container['env'])
    volumes = json.loads(container['local_volumes'])

    host = container['host']
    image, mem_limit, cpuset_cpus, cpuset_mems, network_mode, ports, entrypoint, command = \
        query_container_infos(host, container_id)
    if image == new_image:
        click.echo("host: %s, container: %s is the new image, skip upgrade" % (host, container_name))
        return

    click.echo("Prepare upgrade container: %s" % container_name)
    _pull_images(host, [new_image])

    stop_and_remove_container(host, container_id)
    client = DockerManager.get_client(host)
    if network_mode == 'host':
        new_container = client.containers.run(new_image,
                                              detach=True,
                                              privileged=True,
                                              mem_limit=mem_limit,
                                              volumes=volumes,
                                              command=command,
                                              entrypoint=entrypoint,
                                              environment=envs,
                                              name=container_name,
                                              network_mode=network_mode,
                                              cpuset_cpus=cpuset_cpus,
                                              cpuset_mems=cpuset_mems
                                              )
    else:
        new_container = client.containers.run(new_image,
                                              detach=True,
                                              privileged=True,
                                              mem_limit=mem_limit,
                                              volumes=volumes,
                                              command=command,
                                              entrypoint=entrypoint,
                                              environment=envs,
                                              name=container_name,
                                              ports=ports,
                                              cpuset_cpus=cpuset_cpus,
                                              cpuset_mems=cpuset_mems
                                              )
    dbapi.update_container_id_and_ip(container_name, new_container.short_id,
                                     new_container.attrs['NetworkSettings']['IPAddress'])
    click.echo("Upgrade container: %s success" % container_name)


def query_container_infos(host, container_id):
    client = DockerManager.get_client(host)
    try:
        container = client.containers.get(container_id)
        image = container.attrs['Config']['Image']
        mem_limit = container.attrs['HostConfig']['Memory']
        cpuset_cpus = container.attrs['HostConfig']['CpusetCpus']
        cpuset_mems = container.attrs['HostConfig']['CpusetMems']
        network_mode = container.attrs['HostConfig']['NetworkMode']
        ports = container.attrs['NetworkSettings']['Ports']
        entrypoint = container.attrs['Config']['Entrypoint']
        command = container.attrs['Config']['Cmd']
        return image, mem_limit, cpuset_cpus, cpuset_mems, network_mode, ports, entrypoint, command
    except docker.errors.NotFound:
        click.echo('container: %s is not existing at %s.' % (container_id, host))
        return None


def rm_volumes_if_needed(host, volumes):
    for dir in volumes.keys():
        if "mysql" not in dir and "shared" not in dir and "polarx" not in dir:
            continue
        if "columnar" in dir:
            continue
        if FileManager.exists(host, dir):
            logger.info("rm directory: %s at: %s" % (dir, host))
            FileManager.rmdir(host, dir)


def exec_cmd_for_cn(host, container_name, container_id, cmd):
    client = DockerManager.get_client(host)
    try:
        container = client.containers.get(container_id)
        if container.status != 'running':
            logger.info("container: %s at host: %s is not running" % (container_name, host))
            return None
        (exit_code, output) = container.exec_run(cmd)
        output = output.decode('utf-8').strip()
        if exit_code != 0:
            logger.info("container: %s at host: %s exec cmd failed, output: %s" % (container_name, host, output))
            return None
        return True
    except docker.errors.NotFound:
        click.echo('exec to container: %s fail, at host %s, cmd: %s' % (container_name, host, cmd))
        return None


def check_and_repair_dn(xdb, repair):
    xdb_name = xdb['xdb_name']
    xdb_type = xdb['xdb_type']
    if xdb_type == 'gms':
        return
    xdb_containers = dbapi.list_xdb_containers_by_name(xdb_name)

    expect_leader_container = None
    for xdb_container in xdb_containers:
        container_name = xdb_container['container_name']
        if 'Cand-0-' in container_name:
            expect_leader_container = container_name
            break

    for xdb_container in xdb_containers:
        container_name = xdb_container['container_name']
        container_id = xdb_container['container_id']
        container_host = xdb_container['host']
        role = query_container_role(container_host, container_name, container_id)
        if role != constant.ROLE_LEADER:
            continue
        if container_name == expect_leader_container:
            click.echo("leader is correct, leader container: %s, host: %s"
                       % (container_name, container_host))
        else:
            click.echo("leader container is wrong, leader container: %s, host: %s"
                       % (container_name, container_host))
            if not repair:
                continue
            result = change_leader_container(cur_leader_host=container_host,
                                             cur_leader_container_id=container_id,
                                             cur_leader_container_name=container_name,
                                             expect_leader_container_name=expect_leader_container)
            if result:
                click.echo("succeed to change leader for %s" % expect_leader_container)
            else:
                click.echo("failed to change leader for %s" % expect_leader_container)


def reorder_xdb_containers_for_restart(xdb_name, xdb_containers):
    leader_container = None

    for xdb_container in xdb_containers:
        container_name = xdb_container['container_name']
        container_id = xdb_container['container_id']
        container_host = xdb_container['host']
        role = query_container_role(container_host, container_name, container_id)
        if role == constant.ROLE_LEADER:
            leader_container = xdb_container

    if not leader_container:
        click.echo("can not find leader container for xdb: %s" % xdb_name)
        return None

    xdb_containers.remove(leader_container)
    xdb_containers.append(leader_container)
    return xdb_containers


def _pull_images(host, image_list):
    for image in image_list:
        if not image:
            continue
        click.echo("Pull image: %s at %s" % (image, host))
        client = DockerManager.get_client(host)
        click.echo("\n")
        for info in client.api.pull(image, stream=True, decode=True):
            if 'id' in info:
                progress = info['progress'] if 'progress' in info else ''
                click.echo(info['id'] + ":" + info['status'] + ' ' + progress)
            else:
                click.echo(info['status'])
