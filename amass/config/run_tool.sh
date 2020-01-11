#!/bin/bash
read host
amass enum -d "$host" -dir /amass 2>/dev/null
echo "DONE"
