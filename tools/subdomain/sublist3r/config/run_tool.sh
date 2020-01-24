#!/bin/bash
read host
sublist3r -t 100 -o /sublist3r/sublist3r.out -d $host > /dev/null 2>&1
cat /sublist3r/sublist3r.out
echo "DONE"
