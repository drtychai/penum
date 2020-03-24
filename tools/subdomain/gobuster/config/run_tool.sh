#!/bin/bash
read host
gobuster dns -q -z -t 50 -o /dev/shm/gobuster-${host}.out -w /wl.txt -d $host > /dev/null 2>&1
cat /dev/shm/gobuster-${host}.out | cut -d ' ' -f 2 > /output/subdomain/gobuster-${host}.out
rm /dev/shm/gobuster-${host}.out
echo "DONE"
