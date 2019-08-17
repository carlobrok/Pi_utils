#!/bin/bash
d=`date +%H:%M:%S`

scp -o ConnectTimeout=3 $2 pi@$1:$3
STATUS=$?
if [ $STATUS -eq 0 ]; then
    echo "[$d] Successfully copied latest files!"
    echo "[$d] Rebuild project"
    echo " "
    ssh pi@$1 "cd $3; make all"

    STATUS=$?
    if [ $STATUS -eq 0 ]; then
	echo " "
	echo "[$d] Finished! Build complete!"
    else 
	echo " "
        echo "[$d] Failed. Aborted build!"
    fi
else 
    echo "[$d] Failed to opload files to pi!"
fi

