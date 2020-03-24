#!/bin/bash
read host
#/ng-enum.py ${host} -a -p /altdns/words.txt -f /wl.txt -o /output/subdomain/recon-ng-${host}.out > /dev/null 2>&1
/ng-enum.py ${host} -o /output/subdomain/recon-ng-${host}.out
echo "DONE"
