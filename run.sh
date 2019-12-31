#!/bin/bash
#
#  Author: bynx
#  Description: This is an all-in-one enumeration script for domains and IPs
#
#  ToDo:
#    - Add swtich support for ASNs
#

NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[1;32m'

TARGET_FILE="$1"
JOBS=8
O_DIR="./output"

if [ -z $1 ];then
    echo -e "${RED}[-] Usage: $0 <HOST_FILE> [<OUTPUT_DIR>] [<NUM_OF_THREADS>]${NC}"
    exit 1
fi
if [ ! -z $2 ];then
    O_DIR="$2"
fi
if [ ! -z $3 ];then
    JOBS=$3
fi

echo -e "${GREEN}[+] Setting up output paths...${NC}"
parallel -a ${TARGET_FILE} --jobs ${JOBS} "mkdir -p ${O_DIR}/{}/network/nmap && \
                                           mkdir -p ${O_DIR}/{}/domains && \
                                           mkdir -p ${O_DIR}/{}/http"
#interlace -tL ${TARGET_FILE} -o ${O_DIR} -cL ./src/interlace-init.txt
echo -e "${GREEN}[*] Paths created...${NC}"

# Run core functionality
echo -e "${GREEN}[+] Enumerating hosts...${NC}"
parallel -a ${TARGET_FILE} --jobs ${JOBS} --progress --bar \
        --keep-order --joblog parallel.log --results parallel.out \
        "./src/init.sh {} ${O_DIR}"

