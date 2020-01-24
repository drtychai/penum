#!/bin/bash
read host
export HOME="/root"
subfinder -silent -t 100 -o /subfinder/subfinder.out -d "$host"
echo "DONE"
