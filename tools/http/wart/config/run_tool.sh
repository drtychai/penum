#!/bin/bash
read host

# Get webservers from shared output
TOOL_OUT="/output/http/${host}"
python3 wart.py ${TOOL_OUT}/webservers-${host}.txt

echo "DONE"
