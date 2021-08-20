#!/usr/bin/env bash

# echo "Not implemented yet!"

if [ $# -lt 3 ]; then
    echo "Usage: ./copy.sh <user@source-machine-IP:/path/to/files> <user@target-machine-IP:/path/to/files> <file-1> <file-2> ... <file-N>"
    exit 1
fi

source=$1
target=$2

shift
shift
while [[ $# -gt 0 ]]; do
    curr_file=$source
    curr_file+=$1

	scp $curr_file $target
	
	shift
done