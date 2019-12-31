#!/bin/bash

NC='\033[0m'
RED='\033[0;31m'

HOST="$1"
O_DIR="./output"

if [ -z $1 ]; then
    echo -e "${RED}[-] Usage $0 <HOST> [<OUTPUT_DIR>]${NC}"
    exit 1
fi

if [ ! -z $2 ];then
    O_DIR="$2"
fi

# Setup a switch to choose if nmap or not
if [[ $HOST =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    ./ip-enum.sh  $HOST $O_DIR &
    wait
fi

# Get subdomains and perform DNS flyover
./src/domain-enum.sh $HOST ${O_DIR}/${HOST}/domains &
wait

# Perform HTTP enumeration per discovered webserver
parallel -a ${O_DIR}/${HOST}/http/webservers --progress --bar "./src/http-enum.sh {} ${O_DIR}/${HOST}/http"

