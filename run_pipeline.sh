#!/bin/bash
cd ~/SIEG-Conflicts
source venv/bin/activate

python3 src/scraper.py >> logs/pipeline.log 2>&1
python3 src/processor.py >> logs/pipeline.log 2>&1
bash rotate.sh >> logs/pipeline.log 2>&1
