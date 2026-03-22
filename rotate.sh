#!/bin/bash
BASE=~/SIEG-Conflicts

find $BASE/data/raw -type f -mtime +1 -delete
find $BASE/logs -type f -size +5M -exec truncate -s 0 {} \;

if [ -f $BASE/data/processed/history.csv ]; then
 tail -n 500 $BASE/data/processed/history.csv > $BASE/data/processed/tmp.csv
 mv $BASE/data/processed/tmp.csv $BASE/data/processed/history.csv
fi
