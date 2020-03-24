#!/bin/bash
read host
sublist3r -t 100 -o /output/subdomain/sublist3r-${host}.out -d $host > /dev/null 2>&1
echo "DONE"
