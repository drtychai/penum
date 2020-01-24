#!/bin/bash
read host
$HOME/massdns/subrute.py /wl.txt $host | massdns -r /resolvers.txt -t A -o S -w /massdns/massdns.out > /dev/null 2>&1
cat /massdns/massdns.out
echo "DONE"
