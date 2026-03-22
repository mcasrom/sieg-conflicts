# src/processor.py
# ============================================================
# SIEG — Sistema de Inteligencia Estratégica Global
# Processor v2.0 — detección de países mejorada + scoring + categorías
# © M. Castillo · mybloogingnotes@gmail.com
# ============================================================

import json
import os
import re
import pandas as pd
from datetime import datetime
from utils import add_coords

IN_FILE   = os.path.expanduser("~/SIEG-Conflicts/data/raw/news.json")
OUT_FILE  = os.path.expanduser("~/SIEG-Conflicts/data/processed/conflicts.csv")
HIST_FILE = os.path.expanduser("~/SIEG-Conflicts/data/processed/history.csv")
os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)

# ── MAPA DE ENTIDADES → PAÍS NORMALIZADO ─────────────────────
# Cubre topónimos, gentilicios, organizaciones y zonas conflictivas
ENTITY_MAP = {
    # Oriente Medio
    "israel": "Israel",        "israeli": "Israel",       "jerusalem": "Israel",
    "tel aviv": "Israel",      "netanyahu": "Israel",
    "gaza": "Palestine",       "hamas": "Palestine",      "west bank": "Palestine",
    "rafah": "Palestine",      "palestinian": "Palestine", "ramallah": "Palestine",
    "hezbollah": "Lebanon",    "beirut": "Lebanon",       "lebanon": "Lebanon",
    "iran": "Iran",            "iranian": "Iran",         "tehran": "Iran",
    "khamenei": "Iran",        "irgc": "Iran",
    "iraq": "Iraq",            "iraqi": "Iraq",           "baghdad": "Iraq",
    "mosul": "Iraq",           "erbil": "Iraq",
    "syria": "Syria",          "syrian": "Syria",         "damascus": "Syria",
    "aleppo": "Syria",         "idlib": "Syria",          "deir ez-zor": "Syria",
    "yemen": "Yemen",          "yemeni": "Yemen",         "sanaa": "Yemen",
    "houthi": "Yemen",         "hudaydah": "Yemen",
    "saudi": "Saudi Arabia",   "riyadh": "Saudi Arabia",  "arabia": "Saudi Arabia",
    "jordan": "Jordan",        "amman": "Jordan",
    "turkey": "Turkey",        "turkish": "Turkey",       "ankara": "Turkey",
    "erdogan": "Turkey",       "istanbul": "Turkey",
    "qatar": "Qatar",          "doha": "Qatar",
    "kuwait": "Kuwait",        "bahrain": "Bahrain",      "uae": "UAE",
    "dubai": "UAE",            "abu dhabi": "UAE",
    # Europa del Este / Rusia
    "russia": "Russia",        "russian": "Russia",       "moscow": "Russia",
    "kremlin": "Russia",       "putin": "Russia",         "wagner": "Russia",
    "ukraine": "Ukraine",      "ukrainian": "Ukraine",    "kyiv": "Ukraine",
    "zelensky": "Ukraine",     "kharkiv": "Ukraine",      "donetsk": "Ukraine",
    "mariupol": "Ukraine",     "zaporizhzhia": "Ukraine", "odessa": "Ukraine",
    "crimea": "Ukraine",       "dnipro": "Ukraine",       "kherson": "Ukraine",
    "belarus": "Belarus",      "lukashenko": "Belarus",   "minsk": "Belarus",
    "moldova": "Moldova",      "georgia": "Georgia",      "tbilisi": "Georgia",
    "armenia": "Armenia",      "azerbaijan": "Azerbaijan","nagorno": "Azerbaijan",
    "poland": "Poland",        "warsaw": "Poland",
    "hungary": "Hungary",      "orban": "Hungary",        "budapest": "Hungary",
    "serbia": "Serbia",        "belgrade": "Serbia",      "kosovo": "Kosovo",
    "czech": "Czech Republic", "czechia": "Czech Republic", "prague": "Czech Republic",
    "slovakia": "Slovakia",    "bratislava": "Slovakia",
    "romania": "Romania",      "bucharest": "Romania",
    "bulgaria": "Bulgaria",    "sofia": "Bulgaria",
    "estonia": "Estonia",      "tallinn": "Estonia",
    "latvia": "Latvia",        "riga": "Latvia",
    "lithuania": "Lithuania",  "vilnius": "Lithuania",
    "finland": "Finland",      "helsinki": "Finland",
    "sweden": "Sweden",        "stockholm": "Sweden",
    "norway": "Norway",        "oslo": "Norway",
    "denmark": "Denmark",      "copenhagen": "Denmark",
    "austria": "Austria",      "vienna": "Austria",
    "greece": "Greece",        "athens": "Greece",
    "croatia": "Croatia",      "zagreb": "Croatia",
    "bosnia": "Bosnia",        "sarajevo": "Bosnia",
    # África
    "sudan": "Sudan",          "sudanese": "Sudan",       "khartoum": "Sudan",
    "darfur": "Sudan",         "rsf": "Sudan",
    "ethiopia": "Ethiopia",    "tigray": "Ethiopia",      "addis ababa": "Ethiopia",
    "somalia": "Somalia",      "mogadishu": "Somalia",    "al-shabaab": "Somalia",
    "mali": "Mali",            "bamako": "Mali",          "sahel": "Sahel",
    "burkina": "Burkina Faso", "niger": "Niger",          "nigeria": "Nigeria",
    "libyan": "Libya",         "libya": "Libya",          "tripoli": "Libya",
    "congo": "DR Congo",       "drc": "DR Congo",         "kinshasa": "DR Congo",
    "mozambique": "Mozambique","cabo delgado": "Mozambique",
    "cameroon": "Cameroon",    "chad": "Chad",
    "central african": "CAR",  "car ": "CAR",
    "zimbabwe": "Zimbabwe",    "south africa": "South Africa",
    "egypt": "Egypt",          "cairo": "Egypt",          "sisi": "Egypt",
    "tunisia": "Tunisia",      "algeria": "Algeria",      "morocco": "Morocco",
    # Asia / Pacífico
    "china": "China",          "chinese": "China",        "beijing": "China",
    "xi jinping": "China",     "pla": "China",            "taiwan strait": "Taiwan",
    "taiwan": "Taiwan",        "taipei": "Taiwan",
    "north korea": "N. Korea", "kim jong": "N. Korea",    "pyongyang": "N. Korea",
    "south korea": "S. Korea", "seoul": "S. Korea",
    "japan": "Japan",          "tokyo": "Japan",
    "india": "India",          "indian": "India",         "new delhi": "India",
    "modi": "India",           "kashmir": "India/Pakistan",
    "pakistan": "Pakistan",    "islamabad": "Pakistan",   "imran": "Pakistan",
    "afghanistan": "Afghanistan","kabul": "Afghanistan",  "taliban": "Afghanistan",
    "myanmar": "Myanmar",      "burmese": "Myanmar",      "naypyidaw": "Myanmar",
    "junta": "Myanmar",        "rohingya": "Myanmar",
    "philippines": "Philippines","south china sea": "China/Philippines",
    "indonesia": "Indonesia",  "jakarta": "Indonesia",
    "bangladesh": "Bangladesh","sri lanka": "Sri Lanka",
    # América
    "usa": "USA",              "united states": "USA",    "washington": "USA",
    "biden": "USA",            "trump": "USA",            "pentagon": "USA",
    "venezuela": "Venezuela",  "maduro": "Venezuela",     "caracas": "Venezuela",
    "colombia": "Colombia",    "bogota": "Colombia",      "farc": "Colombia",
    "mexico": "Mexico",        "cartel": "Mexico",        "ciudad juarez": "Mexico",
    "haiti": "Haiti",          "port-au-prince": "Haiti",
    "nicaragua": "Nicaragua",  "ortega": "Nicaragua",
    "cuba": "Cuba",            "havana": "Cuba",          "havana": "Cuba",
    "brazil": "Brazil",        "brasilia": "Brazil",      "lula": "Brazil",
    "ecuador": "Ecuador",      "peru": "Peru",            "bolivia": "Bolivia",
    # Europa Occidental
    "france": "France",        "french": "France",        "paris": "France",
    "macron": "France",
    "germany": "Germany",      "german": "Germany",       "berlin": "Germany",
    "uk": "UK",                "britain": "UK",           "british": "UK",
    "london": "UK",            "sunak": "UK",
    "nato": "NATO",            "eu ": "EU",               "european union": "EU",
    "united nations": "UN",    " un ": "UN",              "security council": "UN",
}

# ── SCORING ───────────────────────────────────────────────────
# Palabras que ANULAN el score alto — contexto no bélico
SCORE_NEGATORS = [
    "election", "vote", "ballot", "poll", "mayor", "municipal",
    "court", "trial", "jury", "lawsuit", "legal", "judge",
    "sport", "football", "soccer", "tennis", "olympic",
    "music", "concert", "festival", "film", "movie", "actor",
    "stock", "market", "economy", "gdp", "inflation", "rate",
]

# Contextos de guerra activa — amplifican el score base
WAR_ZONES = [
    "ukraine", "gaza", "sudan", "yemen", "syria", "mali",
    "sahel", "myanmar", "somalia", "afghanistan", "nagorno",
    "west bank", "donetsk", "kharkiv", "zaporizhzhia",
]

SCORE_HIGH   = ["war", "invasion", "nuclear", "massacre", "genocide", "airstrike",
                "missile strike", "chemical weapon", "biological weapon", "annex",
                "bombing campaign", "ground offensive", "total war"]
SCORE_MED_HI = ["killed", "dead", "casualties", "wounded", "airstrike",
                "drone strike", "rocket attack", "mortar", "shelling",
                "bomb explod", "explosion kill", "siege", "hostage",
                "troops killed", "soldiers dead", "civilian dead"]
SCORE_MED    = ["attack", "offensive", "conflict", "troops", "military operation",
                "sanctions", "blockade", "escalat", "rebel", "insurgent",
                "ceasefire", "coup", "missile", "artillery"]
SCORE_LOW    = ["tension", "protest", "crisis", "diplomat", "negotiat",
                "alliance", "threat", "warning", "concern", "disputed",
                "battle", "fight", "struggle"]  # battle/fight aquí — muy ambiguos

def calc_score(title: str, summary: str = "") -> int:
    text = (title + " " + summary).lower()

    # Si el contexto es claramente no bélico → score máximo 2
    negator_hits = sum(1 for n in SCORE_NEGATORS if n in text)
    war_hits     = sum(1 for w in WAR_ZONES if w in text)
    if negator_hits > 0 and war_hits == 0:
        # Contexto civil/político sin zona de guerra → cap en 2
        return 2 if any(k in text for k in SCORE_LOW + SCORE_MED) else 1

    # Score base por keywords
    if any(k in text for k in SCORE_HIGH):   base = 5
    elif any(k in text for k in SCORE_MED_HI): base = 4
    elif any(k in text for k in SCORE_MED):    base = 3
    elif any(k in text for k in SCORE_LOW):    base = 2
    else: base = 1

    # Bonus por zona de guerra activa confirmada
    if war_hits > 0 and base >= 2:
        base = min(base + 1, 5)

    return base

# ── CATEGORIZACIÓN ────────────────────────────────────────────
CAT_KEYS = {
    "Militar":      ["war", "troops", "military", "army", "navy", "airstrike",
                     "missile", "bomb", "offensive", "soldier", "shelling",
                     "weapon", "drone strike", "artillery", "combat", "invasion",
                     "rocket attack", "ground assault", "bombing", "warplane"],
    "Energético":   ["oil", "gas", "pipeline", "energy", "uranium", "nuclear plant",
                     "lithium", "mineral", "strait", "shipping", "fuel", "refinery"],
    "Diplomático":  ["sanction", "treaty", "alliance", "diplomat", "negotiat",
                     "summit", "nato", "un ", "security council", "embargo",
                     "ceasefire", "agreement", "talks", "envoy"],
    "Humanitario":  ["refugee", "displaced", "famine", "humanitarian", "aid",
                     "civilian", "evacuation", "hospital", "children", "hunger",
                     "massacre", "genocide", "war crime"],
    "Cibernético":  ["cyber", "hack", "ransomware", "disinform", "propaganda",
                     "intelligence", "spy", "surveillance", "leak", "breach"],
    "Político":     ["coup", "election", "vote", "ballot", "protest", "revolt",
                     "uprising", "government", "president", "minister", "parliament",
                     "constitution", "sovereignty", "referendum", "mayor", "municipal",
                     "rally", "demonstration", "campaign", "political", "law", "court",
                     "battle to hold", "socialists", "conservatives", "opposition"],
}

def categorize(text: str) -> str:
    t = text.lower()
    scores = {cat: sum(1 for k in keys if k in t)
              for cat, keys in CAT_KEYS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General"

# ── DETECCIÓN DE PAÍS MEJORADA ────────────────────────────────
def detect_country(title: str, summary: str = "") -> str:
    text = (title + " " + summary).lower()
    # Orden: entidades más específicas primero (más largas)
    for entity in sorted(ENTITY_MAP.keys(), key=len, reverse=True):
        if entity in text:
            return ENTITY_MAP[entity]
    return "Unknown"

# ── PROCESADO ─────────────────────────────────────────────────
with open(IN_FILE, encoding="utf-8") as f:
    raw = json.load(f)

news = raw.get("articles", [])
rows = []
unknown_count = 0

for n in news:
    title   = n.get("title",   "").strip()
    summary = n.get("summary", "").strip()

    pais = detect_country(title, summary)

    # Segunda oportunidad: si sigue Unknown, descartar
    # (el scraper ya filtró por relevancia, pero puede quedar alguno raro)
    if pais == "Unknown":
        unknown_count += 1
        # Guardamos igualmente para no perder datos, pero marcamos
        # como "Unknown" para que el dashboard pueda filtrarlo si se desea

    coords = add_coords(pais)
    score    = calc_score(title, summary)
    categoria = categorize(title + " " + summary)

    rows.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pais":      pais,
        "title":     title,
        "summary":   summary,
        "score":     score,
        "lat":       coords[0] if coords else None,
        "lon":       coords[1] if coords else None,
        "source":    n.get("source", ""),
        "categoria": categoria,
    })

df = pd.DataFrame(rows)

# ── GUARDAR PROCESADO ─────────────────────────────────────────
df.to_csv(OUT_FILE, index=False)

# ── HISTÓRICO (deduplicado por título) ────────────────────────
os.makedirs(os.path.dirname(HIST_FILE), exist_ok=True)
if os.path.exists(HIST_FILE):
    hist_df = pd.read_csv(HIST_FILE)
    hist_df = pd.concat([hist_df, df], ignore_index=True)
    hist_df = hist_df.drop_duplicates(subset=["title"], keep="last")
else:
    hist_df = df.copy()

# Retención máxima 30 días (~47k filas/mes controladas)
hist_df["timestamp"] = pd.to_datetime(hist_df["timestamp"], errors="coerce")
cutoff = datetime.now() - pd.Timedelta(days=30)
hist_df = hist_df[hist_df["timestamp"] > cutoff]

hist_df.to_csv(HIST_FILE, index=False)
print(f"  → Histórico             : {len(hist_df)} registros (últimos 30 días)")

# ── STATS ─────────────────────────────────────────────────────
known   = len(df[df["pais"] != "Unknown"])
cats    = df["categoria"].value_counts().to_dict()
print(f"\n[PROCESSOR] {len(df)} noticias procesadas")
print(f"  → Con país identificado : {known}")
print(f"  → Unknown               : {unknown_count}")
print(f"  → Categorías            : {cats}")
print(f"  → Guardado en           : {OUT_FILE}")
