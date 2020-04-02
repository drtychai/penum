#!/bin/bash
set -e
read host

TOOL_OUT="/output/subdomain"

# Make amass config.ini in real-time using results from tool outputs
cp /config_template.ini /config.ini
if [ -f "${TOOL_OUT}/all-subdomains-${host}.out" ];then
    cat ${TOOL_OUT}/all-subdomains.${host}.out >> /config.ini
fi

amass enum -ip -config /config.ini -d ${host} -json ${TOOL_OUT}/amass-0-${host}.json -dir /amass-0-${host}

# Cleanup
rm /config.ini
echo "DONE"
