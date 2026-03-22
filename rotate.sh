#!/bin/bash
BASE=~/SIEG-Conflicts

# limpiar raw >1 día
find $BASE/data/raw -type f -mtime +1 -delete

# truncar logs >5MB
find $BASE/logs -type f -size +5M -exec truncate -s 0 {} \;

# limitar histórico a 500 filas
if [ -f $BASE/data/processed/history.csv ]; then
 tail -n 500 $BASE/data/processed/history.csv > $BASE/data/processed/tmp.csv
 mv $BASE/data/processed/tmp.csv $BASE/data/processed/history.csv
fi
