#!/bin/bash
# Arguments: [OPTIONS] <ip> <filepath> <project subfolder on pi>
# Example: ./upload_build_project.sh 192.168.20.95 ~/git/KamelPi/ /home/pi/projects/

function usage {
  echo "Usage of upload_build_project.sh"
  echo "     ./upload_build_project.sh [OPTIONS] <ip> <project path> <projects folder on pi>"
  echo ""
  echo "Options:"
  echo "     -h      print this help message"
  echo "     -u      uploads all files; use when the date of the pi files aren't correct"
  echo "     -r      rebuilds the entire project"
  echo "     -j      n threads used to build; default is 1"
  echo ""
  echo "  Example: ./upload_build_project.sh 192.168.20.95 ~/git/KamelPi/ /home/pi/projects/"
}

function valid_ip()
{
    local  ip=$1
    local  stat=1

    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 \
            && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi
    return $stat
}

REBUILD="N"
RSYNC_OPTS=-rzvtu
THREADS="1"


while getopts ":huj:r" opt; do
  case ${opt} in
    h ) usage
        exit ;;
    u ) RSYNC_OPTS=-rzvtI ;;
    r ) REBUILD="Y" ;;
    j ) if ! [[ $OPTARG =~ ^[0-9]+$ ]] ; then
          echo "error: option -j: $OPTARG is not a number" >&2; exit 1
        fi
        THREADS="$OPTARG" ;;
    \? ) echo "Invalid option: -$OPTARG" 1>&2
         usage
         exit ;;
    : )
      echo "Invalid option: $OPTARG requires an argument" 1>&2
      exit ;;
  esac
done
shift $((OPTIND -1))

#echo $RSYNC_OPTS

if [ $# -ne 3 ]; then
  usage
  exit
fi

if ! valid_ip $1; then
  echo "error: $1 is not a valid ip address!"
  echo ""
  usage
  exit
fi


# name of the project, get last foldername of arg 2
project_name="$(basename $2)"

#echo "ip: $1"
#echo "path: $2"
#echo "name: $project_name"
#echo "destination: $3"


echo "[$(date +%H:%M:%S)] Sync project data from $2 to pi@$1:$3$project_name"
echo ""
# sync local files with files on remote device

rsync $RSYNC_OPTS --exclude-from="$2.gitignore" -e ssh $2* pi@$1:$3$project_name

# if sync has been successfully (clean files and) rebuild project

if [ $? -eq 0 ]; then
  echo "Successfully copied files!"
  echo " "

  # if arg -r is given clean and build, else only build
  if [ $REBUILD = "Y" ]; then
    echo "Clean all files, rebuild project"
    echo ""
    ssh -t pi@$1 "cd $3$project_name/Debug; make clean; make all -j$THREADS"
  else
    echo "Rebuild project"
    echo ""
    ssh -t pi@$1 "cd $3$project_name/Debug; make all -j$THREADS"
  fi

  # print success / fail message
  if [ $? -eq 0 ]; then
    echo " "
    echo "[$(date +%H:%M:%S)] Finished! Build complete!"
  else
    echo " "
    echo "[$(date +%H:%M:%S)] Failed. Aborted build!"
  fi
else
  echo "[$(date +%H:%M:%S)] Failed to upload files to pi!"
fi
