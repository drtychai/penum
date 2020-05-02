#!/bin/bash
read host
/ng-enum.py ${host} -a -p /altdns/words.txt -w /wl.txt -o /output/subdomain/recon-ng-${host}.out
echo "DONE"