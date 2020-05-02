#!/bin/bash
read host
TOOL_OUT="/output/http/${host}"
mkdir -p ${TOOL_OUT}

# Parallelize wafw00f across all webservers
cat ${TOOL_OUT}/webserver-${host}.txt | parallel "wafw00f -a -o /dev/shm/wafw00f-${host}-{= s:^.*\/\/::, s:\..*$:: =}.json {}"

jq -s ".[0]=[.[]|add]|.[0]" /dev/shm/wafw00f-${host}-*.json > ${TOOL_OUT}/wafw00f-${host}.json

# Cleanup
rm -rf /dev/shm/*.json 2>/dev/null
echo "DONE"
