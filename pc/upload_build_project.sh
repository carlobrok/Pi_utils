#!/bin/bash
# Arguments: <ip> <filepath> <project subfolder on pi> [-c]
# Example: ./upload_build_project.sh 192.168.20.95 ~/git/KamelPi/ /home/pi/projects/

d=`date +%H:%M:%S`

project_name="$(basename $2)"

#echo "ip: $1"
#echo "path: $2"
#echo "name: $project_name"
#echo "destination: $3"

echo "Sync project data from $2 to $1:$3$project_name"
rsync --progress -ru --exclude-from "$2.gitignore" -e ssh $2* pi@$1:$3$project_name

STATUS=$?
if [ $STATUS -eq 0 ]; then
    echo "[$d] Successfully copied changed files!"
    echo "[$d] Rebuild project"
    echo " "

    if [ "$4" = "-c" ]; then
	echo "clean all files"
        ssh -t pi@$1 "cd $3$project_name/Debug; make clean; make all"
    else
        ssh -t pi@$1 "cd $3$project_name/Debug; make all"
    fi

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

