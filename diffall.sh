#!/usr/bin/env bash
oldversion=`python fetch.py -t mac -p $1 -l | tail -2 | head -1 | awk '{print $1}'`
python fetch.py -t mac -p $1 -b $oldversion -d $2