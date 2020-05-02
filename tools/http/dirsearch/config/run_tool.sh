#!/bin/bash
read host

CPU_COUNT=`parallel --number-of-cpus`
TOOL_OUT="/output/http/${host}"
WL="/wl.txt"

dsearch () {
    # extract the protocol
    local uri=$1
    local proto="$(echo ${uri} | grep :// | sed -e's,^\(.*://\).*,\1,g')"
    local url="$(echo ${uri/$proto/})"
    local hostport="$(echo ${url/$user@/} | cut -d/ -f1)"
    local fqdn="$(echo $hostport | sed -e 's,:.*,,g')"
    local port="$(echo $hostport | sed -e 's,^.*:,:,g' -e 's,.*:\([0-9]*\).*,\1,g' -e 's,[^0-9],,g')"
    if [ -z "${port}" ];then
        if grep -q 's' <<< "$proto"; then
            port="443"
        else
            port="80"
        fi
    fi

    python3 dirsearch.py -u ${uri} -E --json-report /tmp/${fqdn}:${port}.json
}

export -f dsearch
cat ${TOOL_OUT}/webservers-${host}.txt | parallel -j+${CPU_COUNT} dsearch {}

mkdir -p ${TOOL_OUT}/dirsearch
cp /tmp/*.json ${TOOL_OUT}/dirsearch/

# Clean up
rm /tmp/*.json
echo "DONE"
