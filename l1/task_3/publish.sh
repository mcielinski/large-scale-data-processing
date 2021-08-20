#!/usr/bin/env bash

# echo "Not implemented yet!"

# name should look like: marcelci/lsdp_list1_task_3

if [ $# -eq 0 ]; then
    echo "Usage: ./publish.sh </path/to/Dockerfile>"
    exit 1
fi

dockerfile_path=$1

# parent_dir=$(basename "${PWD%/*}")
curr_dir="${PWD##*/}"

dockerhub_user="marcelci"
img_name="lsdp_list1_$curr_dir"
# tag="1.0"

docker build -t ${dockerhub_user}/${img_name} ${dockerfile_path}
docker push ${dockerhub_user}/${img_name}

# echo "$parent_dir"
# echo "$curr_dir"
# echo "$img_name"
# echo "$tag"
# echo "$dockerhub_user"
