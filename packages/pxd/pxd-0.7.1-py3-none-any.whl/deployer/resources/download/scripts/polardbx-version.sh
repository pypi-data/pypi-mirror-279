#!/bin/bash

components=("CN" "DN" "CDC" "COLUMNAR")
image_prefixes=("polardbx-sql" "polardbx-engine" "polardbx-cdc" "polardbx-columnar")

IMAGE_LIST_URL=https://polardbx-opensource.oss-cn-hangzhou.aliyuncs.com/k8s-images/images.list
FILE=images.list
curl -s $IMAGE_LIST_URL -o $FILE

for i in "${!components[@]}"; do
  component=${components[$i]}
  image_prefix=${image_prefixes[$i]}
  latest_image=$(grep "$image_prefix" $FILE | sort -V | tail -n 1)
  echo "$component $latest_image"
done


