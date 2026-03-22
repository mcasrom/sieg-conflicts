#!/bin/bash
# run_pipeline.sh
# ============================================================
# SIEG — Sistema de Inteligencia Estratégica Global
# Pipeline runner v2.0
# © M. Castillo · mybloogingnotes@gmail.com
# ============================================================

source ~/SIEG-Conflicts/venv/bin/activate

LOG_FILE=~/SIEG-Conflicts/logs/cron.log
MAX_LOG=5000

mkdir -p ~/SIEG-Conflicts/logs

# Rotación simple de log
if [ -f "$LOG_FILE" ]; then
    tail -n $MAX_LOG "$LOG_FILE" > "$LOG_FILE.tmp"
    mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

echo "[$(date +'%Y-%m-%d %H:%M:%S')] ── Iniciando pipeline SIEG ──────────────" >> "$LOG_FILE"
echo "[$(date +'%Y-%m-%d %H:%M:%S')] Ejecutando scraper..." >> "$LOG_FILE"
python3 ~/SIEG-Conflicts/src/scraper.py >> "$LOG_FILE" 2>&1

echo "[$(date +'%Y-%m-%d %H:%M:%S')] Ejecutando processor..." >> "$LOG_FILE"
python3 ~/SIEG-Conflicts/src/processor.py >> "$LOG_FILE" 2>&1

echo "[$(date +'%Y-%m-%d %H:%M:%S')] Pipeline finalizado ✅" >> "$LOG_FILE"
echo "[$(date +'%Y-%m-%d %H:%M:%S')] ────────────────────────────────────────" >> "$LOG_FILE"
