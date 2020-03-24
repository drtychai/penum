#!/bin/bash
read host
OUT="/output/subdomain/aiodnsbrute-{host}.json"

aiodnsbrute -t 1024 -r /resolvers.txt -o json -f ${OUT} ${host} > /dev/null 2>&1
#aiodnsbrute --recursive --no-verify -r /resolvers.txt -o json -f $OUT $host

LEN=$(expr `jq length ${OUT}` - 1)
for i in `seq 0 ${LEN}`;do
    subdomain=`jq ".[${i}].domain" ${OUT} | sed 's/"//g'`
    echo ${subdomain} >> /output/subdomain/aiodnsbrute-${host}.out
done

rm ${OUT}
echo "DONE"
