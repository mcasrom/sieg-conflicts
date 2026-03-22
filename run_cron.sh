#!/bin/bash
# run_pipeline.sh - Pipeline completo: scraper + processor

# Directorio del proyecto
cd ~/SIEG-Conflicts || exit

# Activar entorno virtual
source ~/SIEG-Conflicts/venv/bin/activate

# Fecha para logs diarios
NOW=$(date +"%Y%m%d_%H%M")
LOGFILE="logs/cron_$NOW.log"

# Crear logs si no existen
mkdir -p logs

# Ejecutar scraper
echo "[$NOW] Ejecutando scraper..." >> $LOGFILE
python3 src/scraper.py >> $LOGFILE 2>&1

# Ejecutar processor
echo "[$NOW] Ejecutando processor..." >> $LOGFILE
python3 src/processor.py >> $LOGFILE 2>&1

echo "[$NOW] Pipeline finalizado ✅" >> $LOGFILE
