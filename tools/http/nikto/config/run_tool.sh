#!/bin/bash
read host

TOOL_OUT="/output/http/${host}"
CPU_COUNT=`parallel --number-of-cpus`
mkdir -p ${TOOL_OUT}/nikto

run_nikto () {
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
    nikto -h ${uri} -ask no -nointeractive -output ${TOOL_OUT}/nikto/${fqdn}.csv
}

# Parallelize nikto across all webservers w/ 2 jobs per CPU
export -f run_nikto
cat ${TOOL_OUT}/webservers-${host}.txt | parallel -j+${CPU_COUNT} run_nikto {}

echo "DONE"
