# src/scraper.py
# ============================================================
# SIEG — Sistema de Inteligencia Estratégica Global
# Scraper v2.0 — con filtro de relevancia geopolítica
# © M. Castillo · mybloogingnotes@gmail.com
# ============================================================

import feedparser
import json
import os
from datetime import datetime

# ── FEEDS ─────────────────────────────────────────────────────
FEEDS = [
    "http://feeds.reuters.com/Reuters/worldNews",
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.dw.com/rdf/rss-en-world",
    "https://feeds.skynews.com/feeds/rss/world.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
]

OUT = os.path.expanduser("~/SIEG-Conflicts/data/raw/news.json")

# ── FILTRO DE RELEVANCIA GEOPOLÍTICA ──────────────────────────
# Solo pasan noticias que contengan al menos UNA de estas keywords
CONFLICT_KEYWORDS = [
    # Violencia directa
    "war", "attack", "airstrike", "missile", "bomb", "explosion", "strike",
    "troops", "military", "soldiers", "army", "navy", "forces", "weapons",
    "killed", "dead", "casualties", "wounded", "hostage", "siege", "battle",
    "offensive", "invasion", "occupation", "ceasefire", "truce", "combat",
    "drone", "artillery", "rocket", "mortar", "sniper", "ambush",
    # Geopolítica
    "conflict", "crisis", "sanctions", "embargo", "coup", "uprising",
    "protest", "revolt", "insurgency", "terrorist", "militia", "rebel",
    "nuclear", "chemical weapon", "biological", "blockade", "escalation",
    "diplomacy", "treaty", "alliance", "nato", "brics", "un security",
    "geopolit", "sovereignty", "territory", "annexation", "referendum",
    # Energía / recursos estratégicos
    "oil", "gas", "pipeline", "energy", "uranium", "lithium", "mineral",
    "strait", "corridor", "shipping lane", "port", "infrastructure",
    # Humanitario
    "refugee", "displaced", "famine", "humanitarian", "aid", "evacuation",
    "genocide", "massacre", "war crime", "civilian",
    # Zonas calientes
    "gaza", "ukraine", "russia", "israel", "iran", "sudan", "yemen",
    "syria", "iraq", "taiwan", "china sea", "sahel", "mali", "somalia",
    "myanmar", "haiti", "venezuela", "north korea", "pakistan", "kashmir",
    "west bank", "palestine", "hezbollah", "hamas", "isis", "wagner",
    "kharkiv", "kyiv", "mariupol", "donetsk", "crimea", "zaporizhzhia",
    "rafah", "jerusalem", "beirut", "damascus", "aleppo", "mogadishu",
    "khartoum", "tripoli", "kabul", "tehran",
]

def is_relevant(title: str, summary: str) -> bool:
    """Devuelve True si la noticia tiene relevancia geopolítica/conflicto."""
    text = (title + " " + summary).lower()
    return any(kw in text for kw in CONFLICT_KEYWORDS)


# ── SCRAPING ──────────────────────────────────────────────────
data = []
stats = {"total": 0, "filtered": 0, "kept": 0}

for feed_url in FEEDS:
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title   = getattr(entry, "title",   "").strip()
            summary = getattr(entry, "summary", "").strip()
            stats["total"] += 1

            if not is_relevant(title, summary):
                stats["filtered"] += 1
                continue

            data.append({
                "title":   title,
                "summary": summary,
                "source":  feed_url,
                "feed_ts": getattr(entry, "published", ""),
            })
            stats["kept"] += 1

        print(f"[+] {feed_url} → {len(feed.entries)} entradas")
    except Exception as e:
        print(f"[!] Error en feed {feed_url}: {e}")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump({
        "ts":       datetime.now().isoformat(),
        "stats":    stats,
        "articles": data,
    }, f, ensure_ascii=False, indent=2)

print(f"\n[SCRAPER] Total: {stats['total']} | Filtradas: {stats['filtered']} | Guardadas: {stats['kept']}")
