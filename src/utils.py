import pycountry

COUNTRIES = {c.name.lower(): c.name for c in pycountry.countries}

ALIASES = {
    "usa": "United States",
    "uk": "United Kingdom",
    "russia": "Russian Federation",
    "iran": "Iran",
    "israel": "Israel",
    "ukraine": "Ukraine",
    "china": "China"
}

def detect_country(text):
    text = text.lower()

    for key, value in ALIASES.items():
        if key in text:
            return value

    for c in COUNTRIES:
        if c in text:
            return COUNTRIES[c]

    return "Unknown"
