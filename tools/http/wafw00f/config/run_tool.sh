#!/bin/bash
read host
TOOL_OUT="/output/http/${host}"

# Extract FQDNs into newline delineated file for wafw00f consumption
mkdir -p ${TOOL_OUT}

# Forge list to check
cat ${TOOL_OUT}/webservers-${host} | sed 's/\.$//g' > ${TOOL_OUT}/wafw00f-${host}.txt


# Run wafw00f on all subdomains
wafw00f -o ${TOOL_OUT}/wafw00f-${host}.json \
        -i ${TOOL_OUT}/wafw00f-${host}.txt

rm ${TOOL_OUT}/wafw00f-${host}.txt

echo "DONE"

