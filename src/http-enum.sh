#!/bin/bash

function run_nikto()
{
    local DIR="${O_DIR}/nikto"
    mkdir $DIR 2>/dev/null

    echo -e "${GREEN}[+] Running nikto...${NC}"
    nikto -h ${WEB_SERVER} > $DIR/$DOMAIN-nikto.out
}

NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'

if [ -z $1 ] || [ -z $2 ]; then
    echo -e "${RED}[-] Usage $0 <HOST:IP> <OUTPUT_DIR>${NC}"
    exit 1
fi

O_DIR="${2}"
if [[ -z `ls $O_DIR 2>/dev/null` ]]; then
    mkdir -p $O_DIR
fi

WEB_SERVER=$1
DOMAIN=`echo "${WEB_SERVER:0:${#WEB_SERVER}-1}"| sed 's/^http.*:\/\///'`
run_nikto
