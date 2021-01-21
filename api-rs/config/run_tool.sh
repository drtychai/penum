#!/bin/bash
read host

# port scan all TCP ports; discoverd TCP ports get deep scan for TCP+UDP
rustscan --ulimit 10000 -r 0-65525 -a ${host} - -Pn -sS -sC -sV -sU -T4 -oA /rustscan/rustscan-${host} 

#nmap -p- -sS -sC -sV -Pn -T4 -oA /nmap/nmap-${host} $host > /dev/null 2>&1
#cat /nmap/nmap-${host}.xml
echo "DONE"
