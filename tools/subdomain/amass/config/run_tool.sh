#!/bin/bash
set -e
read host

# Amalgamate and sort subdomains from other tools
TOOL_OUT="/output/subdomain"
cat ${TOOL_OUT}/*-${host}.out >> ${TOOL_OUT}/all-${host}.tmp
cat ${TOOL_OUT}/all-${host}.tmp | sort -u > ${TOOL_OUT}/all-${host}

# Allow additional flags
amass enum -ip -d "${host}" -df ${TOOL_OUT}/all-${host} -json ${TOOL_OUT}/amass-${host}.json "$@" 2>/dev/null
echo "DONE"
