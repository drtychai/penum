#!/bin/bash
set -e
read host

# Amalgamate, sort, and resolve subdomains from other tools
TOOL_OUT="/output/subdomain"
M_DNS_OUT="/massdns-output"
cat ${TOOL_OUT}/*-${host}.out >> ${M_DNS_OUT}/massdns-${host}.tmp
cat ${M_DNS_OUT}/massdns-${host}.tmp | sort -u > ${M_DNS_OUT}/massdns-${host}.sorted

# Resolve IPv4
RESOLVE_RETRIES=255
RATE=100000

massdns --processes 8 --hashmap-size ${RATE} --resolve-count ${RESOLVE_RETRIES} -r /resolvers.txt \
        -t A --verify-ip -o J -w ${M_DNS_OUT}/massdns-v4-${host}.out ${M_DNS_OUT}/massdns-${host}.sorted

# Resolve IPv6
massdns --processes 8 --hashmap-size ${RATE} --resolve-count ${RESOLVE_RETRIES} -r /resolvers.txt \
        -t AAAA --verify-ip -o J -w ${M_DNS_OUT}/massdns-v6-${host}.out ${M_DNS_OUT}/massdns-${host}.sorted

cat ${M_DNS_OUT}/massdns-v?-${host}.out* > ${TOOL_OUT}/massdns-${host}.json

# Cleanup
rm ${M_DNS_OUT}/*.tmp
rm ${M_DNS_OUT}/*.sorted
rm ${M_DNS_OUT}/*.out*

echo "DONE"
