#!/usr/bin/env bash

# echo "Not implemented yet!"

if [ $# -eq 0 ]; then
    echo "Usage: ./kill.sh <command>"
    exit 1
fi

cmd="pidof"
for arg in "$@"; do
    cmd+=" $arg"
done

pid_of_cmd=$($cmd)

if [ "$pid_of_cmd" == "" ]; then
    echo "No such process"
else
    echo "Killing processes: $pid_of_cmd"
    kill -9 $pid_of_cmd
fi