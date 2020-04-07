#!/bin/bash
read host

# Get webservers from shared output
TOOL_OUT="/output/http/${host}"
cat ${TOOL_OUT}/webservers-${host}.txt | parallel python3 wart.py {}

echo "DONE"
