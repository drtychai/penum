#!/bin/bash
set -e
read host
# Allow additional flags
exec amass enum -d "$host" -dir /amass "$@" 2>/dev/null
echo "DONE"
