#!/usr/bin/env bash
version_string=`python ../fetch.py -t mac -p $1 -l | tail -2 | head -1`
oldversion=`echo $version_string | awk '{print $3}'`
oldbuildnumber=`echo $version_string | awk '{print $1}'`
folder_name="$1\ $oldversion->10.10"
mkdir -p "$folder_name"
cp "../projects/$1.diff" "$folder_name"
touch "$folder_name/tarballs.txt"
printf "$1 $oldversion - http://opensource.apple.com/tarballs/$1/$1-$oldbuildnumber.tar.gz\n$1 10.10 - http://opensource.apple.com/tarballs/$1/$1-$2.tar.gz" > "$folder_name/tarballs.txt"