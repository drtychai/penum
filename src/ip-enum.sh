#!/bin/bash

function run_nmap ()
{
    nmap -oA $O_DIR/nmap/$HOST $HOST
    #nmap -p- -sC -sV -T4 -oA $O_DIR/nmap/$HOST $HOST
}

function parse_services ()
{
    nmap-parse-output $O_DIR/nmap/$HOST.xml service-names > $O_DIR/services
}


function run_aquatone ()
{
    cd $O_DIR; cat nmap/$HOST.xml | aquatone -nmap
}

NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'

HOST=$1
O_DIR=$2

if [ -z $1 ] || [ -z $2 ]; then
    echo -e "${RED}[-] Usage $0 <HOST>${NC}"
    echo -e "${RED}[-] Usage $0 <HOST> <OUTPUT_DIR>${NC}"
    exit 1
fi

#O_DIR="./output"
#if [ -z `ls $O_DIR` ]; then
#    mkdir $O_DIR
#fi

run_nmap &
wait

# Organize by service
parse_services &
wait
