#!/bin/bash
set -e
read host

# Amalgamate and sort subdomains from other tools
TOOL_OUT="/output/subdomain"

# Make amass config.ini in real-time using results from tool outputs
cp /config_template.ini /config.ini
for d in `cat ${TOOL_OUT}/all-subdomains-${host}.out`;do
    echo "domain = ${d}" >> /config.ini
done

amass enum -active -ip -config /config.ini -d ${host} -json ${TOOL_OUT}/amass-${host}.json -dir /amass

# Cleanup
rm /config.ini
echo "DONE"
