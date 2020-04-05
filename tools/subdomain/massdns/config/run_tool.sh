#!/bin/bash

sort_json ()
{
    local POS=$1
    local TLD="$2"
    local M_DIR="$3"

    local ANSWER_LEN=`expr $(jq -s ".[${POS}].data.answers" ${M_DIR}/massdns-${TLD}.resolved | jq length) - 1`

    if [ ${ANSWER_LEN} -ge 0 ];then
        for j in `seq 0 ${ANSWER_LEN}`;do
            jq -s "{\"fqdn\": .[${POS}].name, \"cname\": .[${POS}].data.answers[${j}].data, \"resolver\": .[${POS}].resolver, \"open_port\":null, \"port_service\":\"\"}" ${M_DIR}/massdns-${TLD}.resolved >> ${M_DIR}/subdomains-${TLD}.json
        done
    fi
}

set -e
read host

# Amalgamate, sort, and resolve subdomains from other tools
TOOL_OUT="/output/subdomain"
M_DNS_OUT="/massdns-output"
RESOLVE_RETRIES=255
RATE=100000

cat ${TOOL_OUT}/*-${host}.out >> ${M_DNS_OUT}/massdns-${host}.tmp
cat ${M_DNS_OUT}/massdns-${host}.tmp | sort -u > ${M_DNS_OUT}/massdns-${host}.sorted

massdns --processes 16 --socket-count 4 --hashmap-size ${RATE} --resolve-count ${RESOLVE_RETRIES} -r /resolvers.txt \
        -t A --verify-ip -o J -w ${M_DNS_OUT}/massdns-v4-${host}.out ${M_DNS_OUT}/massdns-${host}.sorted

massdns --processes 16 --socket-count 4 --hashmap-size ${RATE} --resolve-count ${RESOLVE_RETRIES} -r /resolvers.txt \
        -t AAAA --verify-ip -o J -w ${M_DNS_OUT}/massdns-v6-${host}.out ${M_DNS_OUT}/massdns-${host}.sorted

cat ${M_DNS_OUT}/massdns-v?-${host}.out* > ${M_DNS_OUT}/massdns-${host}.json

# TODO: Add in dedup support
# Remove unresolvable
jq "select(.status == \"NOERROR\")" ${M_DNS_OUT}/massdns-${host}.json > ${M_DNS_OUT}/massdns-${host}.resolved

# Reorganize into pre-db syntax
echo -ne '' > ${M_DNS_OUT}/subdomains-${host}.json
TOTAL_LEN=`expr $(jq ".name" ${M_DNS_OUT}/massdns-${host}.resolved | wc -l | sed 's/ //g') - 1`

export -f sort_json
seq 0 ${TOTAL_LEN} | parallel sort_json {} "${host}" "${M_DNS_OUT}"

# Reorganize into db syntax
jq -s "{\"domain\": \"${host}\", \"subdomain\":.}" ${M_DNS_OUT}/subdomains-${host}.json > ${TOOL_OUT}/subdomains-${host}.json

# Cleanup
rm ${M_DNS_OUT}/*.tmp
rm ${M_DNS_OUT}/*.out*
rm ${M_DNS_OUT}/*.sorted
rm ${M_DNS_OUT}/*.resolved

echo "DONE"
