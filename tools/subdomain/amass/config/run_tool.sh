#!/bin/bash
set -e
read host

# Amalgamate subdomains from other tools
echo '' > /output/subdomain/all-${host}
for f in `ls /output/subdomains | grep "${host}"`; do
    cat ${f} >> /output/subdomain/all-${host}
done

# Allow additional flags
exec amass enum -ip -d "${host}" -df /output/subdomain/all-${host} -json /output/subdomain/amass-${host}.json "$@" 2>/dev/null
echo "DONE"
