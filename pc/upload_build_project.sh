
#!/bin/bash
d=`date +%H:%M:%S`

rsync --progress -ru --exclude-from "$2/.gitignore" -e ssh $2/* pi@$1:$3/$4

STATUS=$?
if [ $STATUS -eq 0 ]; then
    echo "[$d] Successfully copied changed files!"
    echo "[$d] Rebuild project"
    echo " "
    ssh pi@$1 "cd $3/$4/Debug; make all"

    STATUS=$?
    if [ $STATUS -eq 0 ]; then
	echo " "
	echo "[$d] Finished! Build complete!"
    else 
	echo " "
        echo "[$d] Failed. Aborted build!"
    fi
else 
    echo "[$d] Failed to upload files to pi!"
fi

