#!/bin/bash
read host
OUT="/aiodnsbrute/aiodnsbrute.json"

aiodnsbrute --no-verify -t 1024 -r /resolvers.txt -o json -f $OUT $host > /dev/null 2>&1
#aiodnsbrute --recursive --no-verify -r /resolvers.txt -o json -f $OUT $host

LEN=$(expr `jq length $OUT` - 1)
for i in `seq 0 $LEN`;do
    subdomain=`jq ".[${i}].domain" $OUT | sed 's/"//g'`
    echo $subdomain >> /aiodnsbrute/aiodnsbrute.out
done

cat /aiodnsbrute/aiodnsbrute.out
echo "DONE"
