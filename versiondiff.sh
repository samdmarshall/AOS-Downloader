#!/usr/bin/env bash
oldversion=`python ../fetch.py -t mac -p $1 -l | tail -2 | head -1 | awk '{print $3}'`
folder_name="$1 $oldversion->10.10"
mkdir $folder_name
mv "../projects/$1.diff" $folder_name