#!/bin/bash
read host
nmap -p- -sS -sC -sV -Pn -T4 -oA /nmap/nmap-${host} $host 2>/dev/null
echo "DONE"
