#!/bin/bash
# ToDo: Fix this so it can read in entire file --> DB integration would make this far better, no user-input would be needed.
read host
cat $host | aquatone -ports xlarge -out /aquatone
echo "DONE"
