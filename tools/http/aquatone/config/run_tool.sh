#!/bin/bash
read host
TOOL_IN="/output/subdomain"
TOOL_OUT="/output/http/${host}/aquatone"
AQ_OUT="/aquatone"

# Extract FQDNs into newline delineated file for aquatone consumption
mkdir -p ${TOOL_OUT}
jq ".subdomain[].fqdn" ${TOOL_IN}/subdomains-${host}.json | sed 's/"//g' > ${AQ_OUT}/subdomains-${host}.txt

# Run aquatone over all subdomains
cat ${AQ_OUT}/subdomains-${host}.txt | aquatone -threads 16 -ports xlarge -out ${AQ_OUT}

# Cleanup
rm ${AQ_OUT}/subdomains-${host}.txt
mv ${AQ_OUT}/* ${TOOL_OUT}/

echo "DONE"
