#!/bin/bash
# Arguments: <filepath> [-c]
# Example: ./build_cc.sh ~/git/KamelPi/ -c

if [ $# -gt 2 ] || [ $# -lt  1 ]; then
  echo "Usage of build_cc.sh"
  echo "  ./build_cc.sh <filepath> [-c]"
  echo "  Example: ./build_cc.sh ~/git/KamelPi/ -c"
  exit 1
fi

d=`date +%H:%M:%S`

# name of the project, get last foldername of arg 1
project_name="$(basename $1)"


# if arg -c is given clean and build, else only build
if [ "$4" = "-c" ]; then
  make clean all -C "$1Debug" CC=aarch64-rpi3-linux-gnu-g++
else
  make all -C "$1Debug" CC=aarch64-rpi3-linux-gnu-g++
fi
