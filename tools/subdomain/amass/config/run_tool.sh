#!/bin/bash
set -e
read host

# Amalgamate and sort subdomains from other tools
TOOL_OUT="/output/subdomain"
echo "${host}" > ${TOOL_OUT}/all-${host}.tmp
cat ${TOOL_OUT}/*-${host}.out >> ${TOOL_OUT}/all-${host}.tmp
cat ${TOOL_OUT}/all-${host}.tmp | sort -u > ${TOOL_OUT}/all-${host}

# Due to a bug with the -df option, we pass amass a csv of all the 'discovered' domains
tr '\n' ',' < ${TOOL_OUT}/all-${host} > ${TOOL_OUT}/all-${host}.csv
csv_hosts=`cat ${TOOL_OUT}/all-${host}.csv`

# Allow additional flags
amass enum -ip -d "${csv_hosts}" -json ${TOOL_OUT}/amass-${host}.json -dir /amass 2>/dev/null
#amass enum -active -ip -d "${host}" -json ${TOOL_OUT}/amass-${host}.json 2>/dev/null
echo "DONE"
