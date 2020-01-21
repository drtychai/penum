#!/bin/bash
read host
gobuster dns -q -z -t 50 -o /gobuster/gobuster.out -w /wl.txt -d $host > /dev/null 2>&1
cat /gobuster/gobuster.out | cut -d ' ' -f 2
echo "DONE"
