#!/usr/bin/env bash

# echo "Not implemented yet!"

echo "This filter:"
echo "Takes the first 1000 characters (bytes) from /dev/urandom."
echo "Then it removes all but the specified characters: (a-k L-Z 5-9)."
echo "Prints the first 10 of them."

head -c 100 /dev/urandom | LC_ALL=C tr -dc 'a-kL-Z5-9' | head -c 10
echo ""