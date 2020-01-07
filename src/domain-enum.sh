#!/bin/bash

function has_domain ()
{
    # TODO: Add support for CIDR and ASN
    local bool=0
    if [ -z `amass intel -addr $IP` ];then
        $bool=1
    fi
    return $bool
}

function run_subfinder ()
{
    echo -e "${GREEN}[+] Running subfinder...${NC}"
    local OUTPUT="${O_DIR}/${DOMAIN}-subfinder.out"
    local OUTPUT_TMP="${O_DIR}/${DOMAIN}-subfinder-tmp.out"
    local WORDLIST="~/wordlists/domain-bf-wordlist.txt"

    subfinder -recursive -silent -nW -b -w $WORDLIST -t 100 -o $OUTPUT -d $DOMAIN
    subfinder -silent -t 100 -o $OUTPUT_TMP -d $DOMAIN

    cat $OUTPUT_TMP >> $OUTPUT
    rm $OUTPUT_TMP

    if [[ ! -z `cat $OUTPUT 2>/dev/null` ]];then
        cat $OUTPUT >> $D_LIST
    fi
}

function run_sublist3r ()
{
    echo -e "${GREEN}[+] Running sublist3r...${NC}"
    local OUTPUT="${O_DIR}/${DOMAIN}-sublist3r.out"

    sublist3r -b -t 100 -o $OUTPUT -d $DOMAIN
    if [[ ! -z `cat $OUTPUT 2>/dev/null` ]];then
        cat $O_DIR/$DOMAIN-sublist3r.out >> $D_LIST
    fi
}

function run_aiodnsbrute ()
{
    echo -e "${GREEN}[+] Running aiodnsbrute...${NC}"
    local OUTPUT="${O_DIR}/${DOMAIN}-aiodnsbrute.json"
    local OUTPUT_LONG="${O_DIR}/${DOMAIN}-aiodnsbrute-long.json"

    aiodnsbrute --recursive --no-wildcard \
            -r ./resolvers.txt -o json -f $OUTPUT --no-verify $DOMAIN
    aiodnsbrute --recursive --no-wildcard \
            -r ./resolvers.txt -w ~/wordlists/domain-bf-wordlist.txt \
            -o json -f $OUTPUT_LONG --no-verify $DOMAIN

    if [[ ! -z `cat $OUTPUT 2>/dev/null` ]];then
        # Parse JSON for domains and append to mass list
        for i in `seq 1 $(jq length $OUTPUT)`;do
            ip=`cat $OUTPUT | jq ".[$i-1].ip[0]" | tr -d '"'`
            if [ ! "${ip}" == "107.162.150.187" ];then
                name=`cat $OUTPUT | jq ".[$i-1].domain" | tr -d '"'`
                echo $name >> $D_LIST
            fi
        done
    fi

    if [[ ! -z `cat $OUTPUT_LONG 2>/dev/null` ]];then
        # Parse JSON for domains and append to mass list
        for i in `seq 1 $(jq length $OUTPUT_LONG)`;do
            ip=`cat $OUTPUT_LONG | jq ".[$i-1].ip[0]" | tr -d '"'`
            if [ ! "${ip}" == "107.162.150.187" ];then
                name=`cat $OUTPUT_LONG | jq ".[$i-1].domain" | tr -d '"'`
                echo $name >> $D_LIST
            fi
        done
    fi
}

function run_amass ()
{
    echo -e "${GREEN}[+] Running Amass...${NC}"
    amass enum -active -brute -nf $D_LIST -o $O_DIR/$DOMAIN-amass.out -d $DOMAIN
    cat $O_DIR/$DOMAIN-amass.out >> $D_LIST
}

function run_aquatone ()
{
    echo -e "${GREEN}[+] Running aquatone...${NC}"
    if [[ -z `cat $O_DIR/$DOMAIN-amass.out 2>/dev/null` ]];then
        echo -e "${RED}[-] Output from Amass is empty. Cannot run aquatone. Exiting...${NC}"
        exit 1
    fi

    local DIR="${O_DIR}/${DOMAIN}-aquatone"
    if [ -z $DIR ];then
        mkdir $DIR
    fi
    cat $D_LIST | aquatone -ports xlarge -out $DIR

    # Output all URIs to newline delineated file
    cat $DIR/aquatone_session.json |  jq '.pages[] | "\(.url)"' | tr -d '"' > $O_DIR/../http/webservers
}

function sort_domains ()
{
    local TMP="tmp"
    local RGX="^(?=.{4,255}$)([a-zA-Z0-9_]([a-zA-Z0-9_-]{0,61}[a-zA-Z0-9_])?\.){1,126}[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]$"

    # Remove empty lines, duplicates, and syntactically invlaid domains
    sed -i '/^[[:space:]]*$/d' $D_LIST
    sort -u $D_LIST -o $TMP
    grep -P $RGX $TMP > $D_LIST
}

NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[1;32m'

if [ -z $1 ] || [ -z $2 ]; then
    echo -e "${RED}[-] Usage $0 <DOMAIN_NAME> <PATH_TO_OUTPUT_DIR>${NC}"
    exit 1
fi

O_DIR="${2}"
D_LIST="${O_DIR}/all-FQDNs.txt"
if [[ -z `ls $O_DIR 2>/dev/null` ]]; then
    mkdir -p $O_DIR
    touch $D_LIST
else
    echo '' > $D_LIST
fi

DOMAIN=$1
if [[ $DOMAIN =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    IP=$DOMAIN
    if [ has_domains ]; then
        DOMAIN=`amass intel -addr $IP`
    else
        exit 1
    fi
fi

# Run the following concurrently and wait until all complete
run_subfinder &
run_sublist3r &
run_aiodnsbrute &
wait

sort_domains
run_amass

sort_domains
run_aquatone
