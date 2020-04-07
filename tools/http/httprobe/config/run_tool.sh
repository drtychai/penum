#!/bin/bash
read host
TOOL_IN="/output/subdomain"
TOOL_OUT="/output/http/${host}/httprobe"
HP_OUT="/httprobe"

# Extract FQDNs into newline delineated file for httprobe consumption
mkdir -p ${TOOL_OUT}
jq ".subdomain[].fqdn" ${TOOL_IN}/subdomains-${host}.json | sed 's/"//g' > ${HP_OUT}/subdomains-${host}.txt

# Generate additioanl ports params
P_ARG=""
for p in `cat /ports.txt`;do
    P_ARG="${P_ARG}-p http:${p} -p https:${p} "
done

# Run httprobe over all subdomains
cat ${HP_OUT}/subdomains-${host}.txt | httprobe -c 10000 -s ${P_ARG} > ${TOOL_OUT}/httprobe-${host}.txt

echo "DONE"
