#!/bin/bash
read host
nmap -p- -sS -sC -sV -Pn -T4 -oA /nmap/nmap-${host} $host > /dev/null 2>&1
cat /nmap/nmap-${host}.xml
echo "DONE"
