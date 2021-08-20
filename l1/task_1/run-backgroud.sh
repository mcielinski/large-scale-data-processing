#!/usr/bin/env bash

# echo "Not implemented yet!"

echo "Usage: ./run-backgroud.sh <command>"

cmd=""
for arg in "$@"; do
    if [[ "$cmd" != "" ]]; then
        cmd+=" "
    fi
    cmd+="$arg"
done

$cmd &
# eval $cmd &
# jobs