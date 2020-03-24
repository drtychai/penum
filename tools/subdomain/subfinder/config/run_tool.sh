#!/bin/bash
read host
export HOME="/root"
subfinder -silent -t 100 -o /output/subdomain/subfinder-${host}.out -d "$host"
echo "DONE"
