#!/bin/bash
set -e
read host

# Amalgamate, sort, and resolve subdomains from other tools
TOOL_OUT="/output/subdomain"
M_DNS_OUT="/massdns-output"
cat ${TOOL_OUT}/*-${host}.out >> ${M_DNS_OUT}/massdns-${host}.tmp
cat ${M_DNS_OUT}/massdns-${host}.tmp | sort -u > ${M_DNS_OUT}/massdns-${host}.sorted

# Resolve IPv4
massdns --processes 50 -r /resolvers.txt -t A --verify-ip -o S -w ${M_DNS_OUT}/massdns-v4-${host}.out ${M_DNS_OUT}/massdns-${host}.sorted

# Resolve IPv6
massdns --processes 50 -r /resolvers.txt -t AAAA --verify-ip -o S -w ${M_DNS_OUT}/massdns-v6-${host}.out ${M_DNS_OUT}/massdns-${host}.sorted

cat ${M_DNS_OUT}/massdns-v?-${host}.out* > ${M_DNS_OUT}/massdns-all-${host}.out
cat ${M_DNS_OUT}/massdns-all-${host}.out | cut -d ' ' -f 1 | sort -u > ${TOOL_OUT}/all-subdomains-${host}.out
sed -i 's/.$//g' ${TOOL_OUT}/all-subdomains-${host}.out

# Cleanup
rm ${M_DNS_OUT}/*.tmp
rm ${M_DNS_OUT}/*.sorted
rm ${M_DNS_OUT}/*.out*

echo "DONE"
