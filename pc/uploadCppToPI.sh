#!/bin/bash
d=`date +%H:%M:%S`

scp -o ConnectTimeout=3 $2 pi@$1:$3
STATUS=$?
if [ $STATUS -eq 0 ]; then    
    echo "[$d] Übertragung zum PI erfolgreich!"
    echo "[$d] Rebuild" $4
    echo " "
    replace_with=""    	
    ssh pi@$1 "cd $3; mv ${4/.cpp/$replace_with} ${4/.cpp/$replace_with}_backup; make OUT=${4/.cpp/$replace_with}"

    STATUS=$?
    if [ $STATUS -eq 0 ]; then
	echo " "
	echo "[$d] Fertig! Build erfolgreich!"
    else 
	echo " "
        echo "[$d] Fehler. Build abgebrochen!"
    fi
else 
    echo "[$d] Fehler bei der Übertragung zum PI!"
fi

