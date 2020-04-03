#!/bin/bash
set -e
read host

TOOL_OUT="/output/subdomain"

# Make amass config.ini in real-time using results from tool outputs
cp /config_template.ini /config.ini
# Add any special config params here

amass enum -config /config.ini -d ${host} -log /log/${host}.log -o ${TOOL_OUT}/amass-${host}.out

# Cleanup
rm /config.ini
echo "DONE"
