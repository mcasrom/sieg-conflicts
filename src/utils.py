# src/utils.py
# ============================================================
# SIEG — Sistema de Inteligencia Estratégica Global
# Utils v2.0 — coordenadas completas para ~100 países/zonas
# © M. Castillo · mybloogingnotes@gmail.com
# ============================================================

# ── COORDENADAS POR PAÍS/ZONA ─────────────────────────────────
# Formato: "NombreNormalizado": (lat, lon)
# Coordenadas = capital o centroide geográfico del conflicto

PAISES_COORDS = {
    # ── Oriente Medio ──────────────────────────────────────
    "Israel":        (31.77, 35.21),
    "Palestine":     (31.90, 35.30),   # Ramallah / Gaza
    "Gaza":          (31.35, 34.31),
    "Lebanon":       (33.89, 35.50),
    "Syria":         (34.80, 38.99),
    "Iraq":          (33.34, 44.40),
    "Iran":          (35.69, 51.39),
    "Yemen":         (15.55, 48.52),
    "Saudi Arabia":  (24.69, 46.72),
    "Jordan":        (31.95, 35.93),
    "Turkey":        (39.93, 32.86),
    "Qatar":         (25.29, 51.53),
    "Kuwait":        (29.37, 47.98),
    "Bahrain":       (26.07, 50.56),
    "UAE":           (24.47, 54.37),
    "Oman":          (23.61, 58.59),
    # ── Europa del Este / Rusia ────────────────────────────
    "Russia":        (55.75, 37.62),
    "Ukraine":       (50.45, 30.52),
    "Belarus":       (53.90, 27.57),
    "Moldova":       (47.00, 28.86),
    "Georgia":       (41.69, 44.83),
    "Armenia":       (40.18, 44.51),
    "Azerbaijan":    (40.41, 49.87),
    "Poland":        (52.23, 21.01),
    "Hungary":       (47.50, 19.04),
    "Serbia":        (44.80, 20.46),
    "Kosovo":        (42.67, 21.17),
    "Romania":       (44.43, 26.10),
    "Bulgaria":      (42.70, 23.32),
    "Slovakia":      (48.15, 17.11),
    "Czech Republic":(50.08, 14.42),
    "Finland":       (60.17, 24.94),
    "Estonia":       (59.44, 24.75),
    "Latvia":        (56.95, 24.11),
    "Lithuania":     (54.69, 25.28),
    # ── Europa Occidental ──────────────────────────────────
    "France":        (48.86, 2.35),
    "Germany":       (52.52, 13.40),
    "UK":            (51.51, -0.13),
    "Spain":         (40.42, -3.70),
    "Italy":         (41.90, 12.48),
    "NATO":          (50.88, 4.33),    # Bruselas HQ
    "EU":            (50.85, 4.35),
    "UN":            (40.75, -73.97),  # Nueva York
    # ── África ────────────────────────────────────────────
    "Sudan":         (15.55, 32.53),
    "Ethiopia":      (9.03,  38.74),
    "Somalia":       (2.05,  45.34),
    "Kenya":         (-1.29, 36.82),
    "Mali":          (12.65, -8.00),
    "Sahel":         (14.00, 2.00),    # Centroide Sahel
    "Burkina Faso":  (12.37, -1.53),
    "Niger":         (13.51, 2.11),
    "Nigeria":       (9.07,  7.40),
    "Libya":         (32.90, 13.18),
    "DR Congo":      (-4.32, 15.32),
    "CAR":           (4.36,  18.56),
    "Chad":          (12.10, 15.04),
    "Cameroon":      (3.87,  11.52),
    "Mozambique":    (-25.97, 32.59),
    "Zimbabwe":      (-17.83, 31.05),
    "South Africa":  (-25.75, 28.19),
    "Egypt":         (30.06, 31.25),
    "Tunisia":       (36.82, 10.17),
    "Algeria":       (36.74, 3.06),
    "Morocco":       (33.99, -6.85),
    "Eritrea":       (15.33, 38.93),
    "South Sudan":   (4.86,  31.57),
    "Uganda":        (0.32,  32.58),
    "Tanzania":      (-6.17, 35.74),
    "Senegal":       (14.69, -17.44),
    # ── Asia Central / Sur ────────────────────────────────
    "Afghanistan":   (34.52, 69.18),
    "Pakistan":      (33.72, 73.06),
    "India":         (28.61, 77.21),
    "India/Pakistan":(32.00, 76.00),   # Kashmir
    "Bangladesh":    (23.81, 90.41),
    "Sri Lanka":     (6.93,  79.85),
    "Nepal":         (27.71, 85.32),
    "Kazakhstan":    (51.18, 71.45),
    "Uzbekistan":    (41.30, 69.24),
    "Tajikistan":    (38.56, 68.77),
    "Kyrgyzstan":    (42.87, 74.59),
    "Turkmenistan":  (37.95, 58.38),
    # ── Asia Oriental / Pacífico ──────────────────────────
    "China":         (39.91, 116.39),
    "Taiwan":        (25.05, 121.56),
    "China/Philippines": (16.00, 119.00),  # Mar del Sur
    "N. Korea":      (39.02, 125.75),
    "S. Korea":      (37.57, 126.98),
    "Japan":         (35.69, 139.69),
    "Myanmar":       (19.74, 96.08),
    "Thailand":      (13.75, 100.52),
    "Vietnam":       (21.03, 105.85),
    "Philippines":   (14.60, 120.98),
    "Indonesia":     (-6.21, 106.85),
    "Malaysia":      (3.14,  101.69),
    "Cambodia":      (11.56, 104.92),
    # ── América ───────────────────────────────────────────
    "USA":           (38.90, -77.04),
    "Mexico":        (19.43, -99.13),
    "Colombia":      (4.71,  -74.07),
    "Venezuela":     (10.48, -66.88),
    "Brazil":        (-15.78, -47.93),
    "Peru":          (-12.05, -77.04),
    "Ecuador":       (-0.23, -78.52),
    "Bolivia":       (-16.50, -68.15),
    "Argentina":     (-34.62, -58.44),
    "Chile":         (-33.46, -70.65),
    "Paraguay":      (-25.28, -57.63),
    "Haiti":         (18.54, -72.34),
    "Cuba":          (23.13, -82.38),
    "Nicaragua":     (12.13, -86.28),
    "Honduras":      (14.07, -87.21),
    "El Salvador":   (13.69, -89.22),
    "Guatemala":     (14.64, -90.51),
    "Canada":        (45.42, -75.70),
    # ── Otros ─────────────────────────────────────────────
    "Norway":        (59.91, 10.75),
    "Sweden":        (59.33, 18.07),
    "Denmark":       (55.68, 12.57),
    "Austria":       (48.21, 16.37),
    "Switzerland":   (46.95, 7.45),
    "Netherlands":   (52.37, 4.90),
    "Belgium":       (50.85, 4.35),
    "Portugal":      (38.72, -9.14),
    "Greece":        (37.98, 23.73),
    "Croatia":       (45.81, 15.97),
    "Bosnia":        (43.84, 18.36),
    "Albania":       (41.33, 19.82),
    "N. Macedonia":  (41.99, 21.43),
    "Montenegro":    (42.44, 19.26),
    "Australia":     (-35.28, 149.13),
    "New Zealand":   (-41.29, 174.78),
}

# ── FUNCIÓN PRINCIPAL ─────────────────────────────────────────
def add_coords(pais: str):
    """Devuelve (lat, lon) para el país dado.
    Si no se encuentra, devuelve None para que el dashboard lo filtre."""
    return PAISES_COORDS.get(pais, None)


# ── detect_country — versión legacy (compatibilidad) ──────────
# La detección principal está en processor.py v2.0
# Esta función queda como fallback si algo la importa directamente
def detect_country(text: str) -> str:
    text_l = text.lower()
    for country in PAISES_COORDS:
        if country.lower() in text_l:
            return country
    return "Unknown"
