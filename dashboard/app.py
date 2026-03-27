# dashboard/app.py
# ============================================================
# SIEG — Sistema de Inteligencia Estratégica Global
# Radar de Conflictos Globales · Dashboard v2.0
# © M. Castillo · mybloogingnotes@gmail.com
# ============================================================

import os
import math
import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="SIEG · Radar de Conflictos Globales",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "mailto:mybloogingnotes@gmail.com",
        "Report a bug": "https://github.com/mcasrom/sieg-conflicts/issues",
        "About": "**SIEG — Sistema de Inteligencia Estratégica Global**\n\n© M. Castillo · mybloogingnotes@gmail.com",
    },
)

# ── CUSTOM CSS ────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');

/* ── Root palette — verde terminal SIEG */
:root {
    --green:      #00ff41;
    --green-dim:  #00cc33;
    --green-dark: #009922;
    --green-faint:#004411;
    --bg:         #0a0e0a;
    --bg2:        #0f1a0f;
    --bg3:        #111a11;
    --text:       #c8ffc8;
    --muted:      #4a7a4a;
    --border:     #1a3a1a;
    --accent-2:   #ff4040;
    --accent-3:   #ffa500;
    --accent-ok:  #00e676;
}

/* ── Global reset */
html, body, [class*="css"] {
    font-family: 'Courier New', Courier, monospace !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Scanlines */
body::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,255,65,0.015) 2px, rgba(0,255,65,0.015) 4px
    );
    pointer-events: none;
    z-index: 1000;
}

/* ── Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 2rem 2rem 2rem !important; }

/* ── Header bar */
.sieg-header {
    background: var(--bg2);
    border-bottom: 1px solid var(--green-faint);
    border-left: 3px solid var(--green);
    padding: 0.8rem 1.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.2rem;
}
.sieg-logo {
    font-family: 'Courier New', monospace;
    font-size: 1.6rem;
    font-weight: bold;
    letter-spacing: 0.3rem;
    color: var(--green);
}
.sieg-logo span { color: var(--muted); }
.sieg-tagline {
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 0.15rem;
    text-transform: uppercase;
}
.sieg-timestamp {
    font-size: 0.75rem;
    color: var(--green-dark);
    opacity: 0.8;
}

/* ── KPI Cards */
.kpi-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-top: 2px solid var(--green);
    padding: 1rem 1.2rem;
    position: relative;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: bold;
    line-height: 1;
    color: var(--green);
}
.kpi-label {
    font-size: 0.62rem;
    letter-spacing: 0.12rem;
    color: var(--muted);
    text-transform: uppercase;
    margin-top: 0.25rem;
}
.kpi-delta {
    font-size: 0.85rem;
    font-weight: bold;
    margin-top: 0.2rem;
}
.kpi-icon {
    position: absolute;
    top: 0.8rem; right: 1rem;
    font-size: 1.2rem;
    opacity: 0.15;
}

/* ── Risk badge */
.risk-high   { color: var(--accent-2);  font-weight: bold; }
.risk-medium { color: var(--accent-3);  font-weight: bold; }
.risk-low    { color: var(--accent-ok); font-weight: bold; }

/* ── Section headers */
.section-title {
    font-size: 0.85rem;
    font-weight: bold;
    letter-spacing: 0.2rem;
    text-transform: uppercase;
    color: var(--green);
    border-left: 3px solid var(--green);
    padding-left: 0.6rem;
    margin: 1.4rem 0 0.8rem 0;
}
.section-title::before { content: '// '; color: var(--muted); }

/* ── Alert box */
.alert-box {
    background: rgba(255,64,64,0.06);
    border: 1px solid rgba(255,64,64,0.3);
    border-left: 3px solid var(--accent-2);
    padding: 0.7rem 1rem;
    font-size: 0.8rem;
    color: #ffaaaa;
    margin: 0.4rem 0;
}

/* ── Info box */
.info-box {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--green-dark);
    padding: 0.7rem 1rem;
    font-size: 0.82rem;
    color: var(--text);
    margin: 0.4rem 0;
}

/* ── Alliance pills */
.pill {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    font-size: 0.68rem;
    font-weight: bold;
    letter-spacing: 0.05rem;
    margin: 0.1rem;
    border: 1px solid;
}
.pill-nato   { background: rgba(0,255,65,0.08);  color: var(--green-dim);  border-color: var(--green-faint); }
.pill-brics  { background: rgba(255,165,0,0.08); color: #ffa500;           border-color: rgba(255,165,0,0.3); }
.pill-eu     { background: rgba(0,255,65,0.05);  color: var(--green-dark); border-color: var(--green-faint); }
.pill-other  { background: rgba(74,122,74,0.1);  color: var(--muted);      border-color: var(--border); }

/* ── Sidebar */
section[data-testid="stSidebar"] > div {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stMarkdown { color: var(--text) !important; }

/* ── Dataframe */
.stDataFrame { border: 1px solid var(--border) !important; }

/* ── Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2);
    border-bottom: 1px solid var(--border);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.82rem;
    letter-spacing: 0.08rem;
    color: var(--muted) !important;
    padding: 0.5rem 1rem;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: var(--green) !important;
    border-bottom: 2px solid var(--green) !important;
    background: transparent !important;
}

/* ── Progress bars */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--green-dark), var(--green)) !important;
}

/* ── Footer */
.sieg-footer {
    text-align: center;
    font-size: 0.65rem;
    color: var(--muted);
    padding: 1.5rem 0 0.5rem 0;
    border-top: 1px solid var(--border);
    letter-spacing: 0.1rem;
    margin-top: 2rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── CONSTANTS ─────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "conflicts.csv")
NOW = datetime.datetime.now(datetime.UTC)

ALLIANCE_MAP = {
    "USA": ["nato", "eu"], "France": ["nato", "eu"], "Germany": ["nato", "eu"],
    "UK": ["nato"], "Turkey": ["nato"], "Poland": ["nato", "eu"],
    "Russia": ["brics"], "China": ["brics"], "India": ["brics"],
    "Brazil": ["brics"], "Iran": ["brics"], "Israel": [],
    "Ukraine": [], "Syria": [], "Yemen": [], "Sudan": [],
    "Arabia Saudí": ["other"], "Pakistan": ["other"],
}

ENERGY_RELEVANCE = {
    "Russia": 10, "Iran": 9, "Arabia Saudí": 10, "China": 8, "USA": 7,
    "Ukraine": 7, "Syria": 5, "Iraq": 8, "Yemen": 6, "Libya": 7,
    "Israel": 4, "Sudan": 3,
}


# ── DATA LOADERS ──────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data():
    if not os.path.exists(DATA_FILE):
        demo = pd.DataFrame(
            {
                "timestamp": pd.date_range(end=NOW, periods=40, freq="6h"),
                "pais": [
                    "Russia", "Ukraine", "Gaza", "Israel", "Sudan", "Yemen",
                    "China", "Taiwan", "Iran", "USA", "Syria", "Mali",
                    "Sahel", "Myanmar", "Ethiopia", "Haiti", "México",
                    "Venezuela", "Armenia", "Azerbaiyán",
                ] * 2,
                "title": [f"Incidente estratégico #{i}" for i in range(40)],
                "summary": ["Sin datos de pipeline — modo demo" for _ in range(40)],
                "score": np.random.randint(1, 15, 40),
                "source": np.random.choice(
                    ["Reuters", "BBC", "AP", "Al Jazeera", "EFE", "DW"], 40
                ),
                "lat": np.random.uniform(-50, 70, 40),
                "lon": np.random.uniform(-120, 140, 40),
                "categoria": np.random.choice(
                    ["Militar", "Diplomático", "Energético", "Humanitario", "Cibernético"],
                    40,
                ),
            }
        )
        return demo, True

    df = pd.read_csv(DATA_FILE)
    for col in ["lat", "lon", "score"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if "categoria" not in df.columns:
        df["categoria"] = "No clasificado"
    return df.dropna(subset=["lat", "lon", "score"]), False


# ── HELPER FUNCTIONS ──────────────────────────────────────────
def risk_label(score):
    if score >= 10:
        return "🔴 CRÍTICO"
    elif score >= 7:
        return "🟠 ALTO"
    elif score >= 4:
        return "🟡 MEDIO"
    else:
        return "🟢 BAJO"


def risk_class(score):
    if score >= 10:
        return "risk-high"
    elif score >= 4:
        return "risk-medium"
    else:
        return "risk-low"


def alliance_pills(country):
    alliances = ALLIANCE_MAP.get(country, [])
    html = ""
    for a in alliances:
        css = f"pill-{a}" if a in ["nato", "brics", "eu"] else "pill-other"
        html += f'<span class="pill {css}">{a.upper()}</span>'
    return html or '<span class="pill pill-other">INDEP.</span>'


def kpi_card(value, label, icon="📊", delta=None, delta_color="var(--accent-ok)"):
    delta_html = (
        f'<div class="kpi-delta" style="color:{delta_color}">{delta}</div>'
        if delta
        else ""
    )
    return f"""
<div class="kpi-card">
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-value">{value}</div>
  <div class="kpi-label">{label}</div>
  {delta_html}
</div>
"""


# ══════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════
df, demo_mode = load_data()

# ── HEADER ────────────────────────────────────────────────────
st.markdown(
    f"""
<div class="sieg-header">
  <div>
    <div class="sieg-logo">SIEG<span> · </span>CONFLICTOS</div>
    <div class="sieg-tagline">Sistema de Inteligencia Estratégica Global — Módulo de Conflictos</div>
  </div>
  <div class="sieg-timestamp">root@sieg:~$ ./conflicts --status &nbsp;·&nbsp; UTC {NOW.strftime('%Y-%m-%d %H:%M')}</div>
</div>
""",
    unsafe_allow_html=True,
)

if demo_mode:
    st.markdown(
        '<div class="alert-box">⚠ MODO DEMO — Pipeline no ejecutado o datos no encontrados en <code>'
        + DATA_FILE
        + "</code></div>",
        unsafe_allow_html=True,
    )

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### **SIEG · FILTROS**")
    st.markdown("---")

    all_countries = sorted(df["pais"].dropna().unique().tolist())
    sel_countries = st.multiselect("🌐 Países", all_countries, default=all_countries)

    score_range = st.slider(
        "⚠️ Rango de riesgo (score)",
        int(df["score"].min()),
        int(df["score"].max()),
        (int(df["score"].min()), int(df["score"].max())),
    )

    if "categoria" in df.columns:
        cats = sorted(df["categoria"].dropna().unique().tolist())
        sel_cats = st.multiselect("🏷️ Categoría", cats, default=cats)
    else:
        sel_cats = None

    if "source" in df.columns:
        sources = sorted(df["source"].dropna().unique().tolist())
        sel_sources = st.multiselect("📡 Fuente", sources, default=sources)
    else:
        sel_sources = None

    st.markdown("---")
    st.markdown(
        """
<div style="font-size:0.65rem;color:#4a7a4a;line-height:1.8;">
METODOLOGÍA SIEG<br>
─────────────────<br>
+ Score = intensidad × frecuencia<br>
+ Datos: RSS / GDELT / ACLED<br>
+ Actualización: cada hora (:55)<br>
+ NLP: RoBERTa-es (bne)<br>
<br>
© M. Castillo<br>
github.com/mcasrom/sieg-conflicts
</div>
""",
        unsafe_allow_html=True,
    )

# ── FILTER DATA ───────────────────────────────────────────────
mask = df["score"].between(score_range[0], score_range[1])
if sel_countries:
    mask &= df["pais"].isin(sel_countries)
if sel_cats and "categoria" in df.columns:
    mask &= df["categoria"].isin(sel_cats)
if sel_sources and "source" in df.columns:
    mask &= df["source"].isin(sel_sources)
dff = df[mask].copy()

# ── KPI ROW ───────────────────────────────────────────────────
st.markdown('<div class="section-title">INDICADORES CLAVE · KPIs ESTRATÉGICOS</div>', unsafe_allow_html=True)

total_news      = len(dff)
total_countries = dff["pais"].nunique()
total_score     = int(dff["score"].sum())
avg_score       = round(dff["score"].mean(), 1) if len(dff) > 0 else 0
critical_zones  = int((dff.groupby("pais")["score"].sum() >= 10).sum())
max_risk_country= dff.groupby("pais")["score"].sum().idxmax() if len(dff) > 0 else "N/A"

energy_scores   = dff[dff["pais"].isin(ENERGY_RELEVANCE)]["pais"].map(ENERGY_RELEVANCE)
energy_index    = int(energy_scores.sum()) if len(energy_scores) > 0 else 0

cols = st.columns(7)
kpis = [
    (total_news,        "Noticias procesadas",     "📰", None, "var(--green)"),
    (total_countries,   "Países en conflicto",     "🌐", None, "var(--accent-3)"),
    (total_score,       "Índice tensión global",   "⚡", None, "var(--accent-2)"),
    (avg_score,         "Score medio/evento",      "📈", None, "var(--accent-ok)"),
    (critical_zones,    "Zonas críticas",          "🔴", None, "var(--accent-2)"),
    (energy_index,      "Índice energético-riesgo","⚡", None, "var(--accent-3)"),
    (max_risk_country,  "País más crítico",        "🚨", None, "var(--accent-2)"),
]
for col, (val, lbl, icon, delta, color) in zip(cols, kpis):
    col.markdown(kpi_card(val, lbl, icon, delta, color), unsafe_allow_html=True)

st.markdown("---")

# ── TABS ──────────────────────────────────────────────────────
tabs = st.tabs([
    "🗺️ MAPA GLOBAL",
    "📊 RIESGO POR PAÍS",
    "🤝 ALIANZAS & GEOPOLÍTICA",
    "⚡ ENERGÍA & RECURSOS",
    "📰 NOTICIAS & FEEDS",
    "📈 TENDENCIAS",
    "ℹ️ METODOLOGÍA",
])

# ── PLOT THEME DEFAULTS ───────────────────────────────────────
_layout = dict(
    plot_bgcolor="rgba(15,26,15,0.7)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c8ffc8", family="Courier New"),
    xaxis=dict(showgrid=True, gridcolor="#1a3a1a"),
    yaxis=dict(showgrid=True, gridcolor="#1a3a1a"),
    legend=dict(bgcolor="rgba(15,26,15,0.8)", bordercolor="#1a3a1a"),
)

# ── TAB 1 — MAPA ──────────────────────────────────────────────
with tabs[0]:
    st.markdown('<div class="section-title">MAPA INTERACTIVO DE CONFLICTOS</div>', unsafe_allow_html=True)

    map_col, detail_col = st.columns([3, 1])

    with map_col:
        fig_map = px.scatter_map(
            dff,
            lat="lat", lon="lon",
            hover_name="title",
            hover_data={"pais": True, "score": True, "source": True, "lat": False, "lon": False},
            color="score",
            size="score",
            size_max=30,
            zoom=1,
            center={"lat": 25, "lon": 15},
            color_continuous_scale=["#009922", "#ffa500", "#ff4040"],
            map_style="carto-darkmatter",
        )
        fig_map.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_colorbar=dict(
                title=dict(text="Score", font=dict(color="#00ff41", family="Courier New")),
                tickfont=dict(color="#c8ffc8", family="Courier New"),
                bgcolor="rgba(15,26,15,0.85)",
                bordercolor="#1a3a1a",
            ),
            height=520,
        )
        st.plotly_chart(fig_map, width="stretch")

    with detail_col:
        st.markdown("**Top 10 puntos calientes**")
        top10 = (
            dff.groupby("pais")
            .agg(score=("score", "sum"), eventos=("score", "count"))
            .reset_index()
            .nlargest(10, "score")
        )
        top10["nivel"] = top10["score"].apply(risk_label)
        for _, row in top10.iterrows():
            cls = risk_class(row["score"])
            st.markdown(
                f'<div style="padding:0.3rem 0;border-bottom:1px solid #1a3a1a;font-size:0.78rem;">'
                f'<span class="{cls}">{row["nivel"]}</span> &nbsp;'
                f'<b style="color:#c8ffc8">{row["pais"]}</b>'
                f'<span style="color:#4a7a4a;float:right;font-family:\'Courier New\',monospace">{int(row["score"])}</span></div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">MAPA DE CALOR — DENSIDAD DE CONFLICTOS</div>', unsafe_allow_html=True)
    fig_heat = go.Figure(go.Densitymap(
        lat=dff["lat"], lon=dff["lon"],
        z=dff["score"], radius=40,
        colorscale="Hot", showscale=True,
        hoverinfo="skip",
    ))
    fig_heat.update_layout(
        map_style="carto-darkmatter",
        mapbox_zoom=1, mapbox_center={"lat": 20, "lon": 10},
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        height=380,
    )
    st.plotly_chart(fig_heat, width="stretch")


# ── TAB 2 — RIESGO POR PAÍS ───────────────────────────────────
with tabs[1]:
    st.markdown('<div class="section-title">ANÁLISIS DE RIESGO POR PAÍS</div>', unsafe_allow_html=True)

    pais_riesgo = dff.groupby("pais").agg(
        score_total=("score", "sum"),
        eventos=("score", "count"),
        score_max=("score", "max"),
    ).reset_index().sort_values("score_total", ascending=False)

    pais_riesgo["nivel"]    = pais_riesgo["score_total"].apply(risk_label)
    pais_riesgo["alianzas"] = pais_riesgo["pais"].apply(alliance_pills)
    pais_riesgo["energia_idx"] = pais_riesgo["pais"].map(ENERGY_RELEVANCE).fillna(0).astype(int)

    left, right = st.columns([2, 1])

    with left:
        fig_bar = go.Figure()
        colors = ["#ff4040" if s >= 10 else "#ffa500" if s >= 4 else "#00e676"
                  for s in pais_riesgo["score_total"]]
        fig_bar.add_trace(go.Bar(
            x=pais_riesgo["pais"],
            y=pais_riesgo["score_total"],
            marker_color=colors,
            marker_line_color="rgba(0,0,0,0)",
            text=pais_riesgo["score_total"],
            textposition="outside",
            textfont=dict(color="#c8ffc8", family="Courier New", size=10),
            hovertemplate="<b>%{x}</b><br>Score: %{y}<extra></extra>",
        ))
        fig_bar.update_layout(
            **_layout,
            xaxis=dict(showgrid=False, tickangle=-35, tickfont=dict(size=10), gridcolor="#1a3a1a"),
            margin=dict(l=0, r=0, t=20, b=60),
            height=400,
        )
        st.plotly_chart(fig_bar, width="stretch")

    with right:
        top6 = pais_riesgo.head(6)
        categories = ["Score total", "Eventos", "Score máx", "Riesgo energ."]
        fig_radar = go.Figure()
        for _, row in top6.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row["score_total"], row["eventos"] * 2,
                   row["score_max"] * 3, row["energia_idx"] * 5],
                theta=categories, fill="toself", name=row["pais"],
                opacity=0.6,
            ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="rgba(15,26,15,0.6)",
                radialaxis=dict(visible=True, color="#1a3a1a"),
                angularaxis=dict(color="#4a7a4a"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c8ffc8", family="Courier New"),
            legend=dict(bgcolor="rgba(15,26,15,0.7)", bordercolor="#1a3a1a"),
            margin=dict(l=10, r=10, t=30, b=10),
            height=400,
        )
        st.plotly_chart(fig_radar, width="stretch")

    st.markdown('<div class="section-title">TABLA DE RIESGO DETALLADA</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="info-box">Semáforo: '
        '<span class="risk-high">🔴 CRÍTICO ≥10</span> · '
        '<span class="risk-medium">🟠 ALTO ≥7 · 🟡 MEDIO ≥4</span> · '
        '<span class="risk-low">🟢 BAJO &lt;4</span></div>',
        unsafe_allow_html=True,
    )

    table_rows = []
    for _, row in pais_riesgo.iterrows():
        table_rows.append({
            "País": row["pais"],
            "Score Total": int(row["score_total"]),
            "Eventos": int(row["eventos"]),
            "Score Máx": int(row["score_max"]),
            "Nivel": row["nivel"],
            "Energía": "⚡" * min(int(row["energia_idx"]), 10),
        })
    st.dataframe(pd.DataFrame(table_rows), width="stretch", hide_index=True)


# ── TAB 3 — ALIANZAS & GEOPOLÍTICA ────────────────────────────
with tabs[2]:
    st.markdown('<div class="section-title">BLOQUES GEOPOLÍTICOS & ALIANZAS</div>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    def bloc_kpi(members_in_data, label, color):
        return f"""
<div class="kpi-card" style="border-top-color:{color}">
  <div class="kpi-value" style="color:{color}">{len(members_in_data)}</div>
  <div class="kpi-label">{label}</div>
</div>"""

    nato_in  = [c for c in dff["pais"].unique() if "nato"  in ALLIANCE_MAP.get(c, [])]
    brics_in = [c for c in dff["pais"].unique() if "brics" in ALLIANCE_MAP.get(c, [])]
    eu_in    = [c for c in dff["pais"].unique() if "eu"    in ALLIANCE_MAP.get(c, [])]

    col_a.markdown(bloc_kpi(nato_in,  "Países OTAN en conflicto", "#00ff41"), unsafe_allow_html=True)
    col_b.markdown(bloc_kpi(brics_in, "Países BRICS en conflicto","#ffa500"), unsafe_allow_html=True)
    col_c.markdown(bloc_kpi(eu_in,    "Países UE en conflicto",   "#00cc33"), unsafe_allow_html=True)

    def bloc_score(members):
        return dff[dff["pais"].isin(members)]["score"].sum()

    bloc_data = pd.DataFrame({
        "Bloque": ["OTAN", "BRICS", "UE", "Sin bloque"],
        "Score":  [
            bloc_score(nato_in), bloc_score(brics_in), bloc_score(eu_in),
            bloc_score([c for c in dff["pais"].unique()
                        if not any(b in ALLIANCE_MAP.get(c, []) for b in ["nato", "brics", "eu"])]),
        ],
        "Color": ["#00ff41", "#ffa500", "#00cc33", "#4a7a4a"],
    })

    fig_bloc = go.Figure(go.Bar(
        x=bloc_data["Bloque"], y=bloc_data["Score"],
        marker_color=bloc_data["Color"],
        text=bloc_data["Score"], textposition="outside",
        textfont=dict(color="#c8ffc8", family="Courier New"),
    ))
    fig_bloc.update_layout(
        **_layout,
        xaxis=dict(showgrid=False, gridcolor="#1a3a1a"),
        margin=dict(l=0, r=0, t=20, b=20), height=300,
    )
    st.plotly_chart(fig_bloc, width="stretch")

    st.markdown('<div class="section-title">MAPA DE ALIANZAS POR PAÍS</div>', unsafe_allow_html=True)
    ally_rows = []
    for _, row in pais_riesgo.iterrows():
        ally_rows.append({
            "País": row["pais"], "Score": int(row["score_total"]),
            "Alianzas": row["alianzas"], "Nivel": row["nivel"],
        })
    ally_df = pd.DataFrame(ally_rows)

    html_table = '<table style="width:100%;border-collapse:collapse;font-size:0.82rem;font-family:\'Courier New\',monospace;">'
    html_table += '<thead><tr style="border-bottom:1px solid #1a3a1a;color:#00ff41;font-size:0.7rem;letter-spacing:0.1rem;">'
    for col in ["PAÍS", "SCORE", "ALIANZAS", "NIVEL"]:
        html_table += f"<th style='padding:0.4rem 0.6rem;text-align:left'>{col}</th>"
    html_table += "</tr></thead><tbody>"
    for _, row in ally_df.iterrows():
        html_table += f"""<tr style="border-bottom:1px solid #0f1a0f;">
          <td style="padding:0.35rem 0.6rem;color:#c8ffc8;font-weight:bold">{row['País']}</td>
          <td style="padding:0.35rem 0.6rem;color:#00ff41">{row['Score']}</td>
          <td style="padding:0.35rem 0.6rem">{row['Alianzas']}</td>
          <td style="padding:0.35rem 0.6rem">{row['Nivel']}</td>
        </tr>"""
    html_table += "</tbody></table>"
    st.markdown(html_table, unsafe_allow_html=True)


# ── TAB 4 — ENERGÍA ───────────────────────────────────────────
with tabs[3]:
    st.markdown('<div class="section-title">IMPACTO ENERGÉTICO & RECURSOS ESTRATÉGICOS</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="info-box">El <b>Índice de Riesgo Energético SIEG</b> pondera la relevancia '
        'geoenergética de cada país (producción/tránsito de petróleo, gas, minerales críticos) '
        'multiplicada por el score de conflicto activo.</div>',
        unsafe_allow_html=True,
    )

    energy_df = dff[dff["pais"].isin(ENERGY_RELEVANCE)].copy()
    energy_df["energia_idx"]  = energy_df["pais"].map(ENERGY_RELEVANCE)
    energy_df["risk_energy"]  = energy_df["score"] * energy_df["energia_idx"]

    energy_country = energy_df.groupby("pais").agg(
        score_total=("score", "sum"),
        energia_idx=("energia_idx", "first"),
        risk_energy=("risk_energy", "sum"),
    ).reset_index().sort_values("risk_energy", ascending=False)

    fig_bubble = go.Figure(go.Scatter(
        x=energy_country["score_total"],
        y=energy_country["energia_idx"],
        mode="markers+text",
        marker=dict(
            size=energy_country["risk_energy"] / energy_country["risk_energy"].max() * 60 + 10,
            color=energy_country["risk_energy"],
            colorscale=["#009922", "#ffa500", "#ff4040"],
            showscale=True,
            colorbar=dict(
                title=dict(text="Riesgo Energético", font=dict(color="#00ff41")),
                tickfont=dict(color="#c8ffc8"),
            ),
            line=dict(color="rgba(0,255,65,0.3)", width=1),
        ),
        text=energy_country["pais"],
        textposition="top center",
        textfont=dict(color="#c8ffc8", size=10),
        hovertemplate="<b>%{text}</b><br>Score conflicto: %{x}<br>Índice energético: %{y}<extra></extra>",
    ))
    fig_bubble.update_layout(
        **_layout,
        xaxis=dict(title="Score de Conflicto", showgrid=True, gridcolor="#1a3a1a"),
        yaxis=dict(title="Relevancia Energética (0-10)", showgrid=True, gridcolor="#1a3a1a"),
        margin=dict(l=20, r=20, t=20, b=40), height=420,
    )
    st.plotly_chart(fig_bubble, width="stretch")

    st.markdown('<div class="section-title">RANKING RIESGO ENERGÉTICO CONSOLIDADO</div>', unsafe_allow_html=True)
    max_re = energy_country["risk_energy"].max()
    for _, row in energy_country.iterrows():
        pct = int(row["risk_energy"] / max_re * 100) if max_re > 0 else 0
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;">'
            f'<span style="width:110px;font-size:0.8rem;font-weight:bold;color:#c8ffc8">{row["pais"]}</span>'
            f'<div style="flex:1;background:#0f1a0f;border:1px solid #1a3a1a;height:16px;position:relative;">'
            f'<div style="width:{pct}%;height:100%;background:linear-gradient(90deg,#009922,#00ff41);"></div>'
            f'</div>'
            f'<span style="width:40px;text-align:right;font-family:\'Courier New\',monospace;font-size:0.75rem;color:#00ff41">{int(row["risk_energy"])}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── TAB 5 — NOTICIAS ──────────────────────────────────────────
with tabs[4]:
    st.markdown('<div class="section-title">FEED DE NOTICIAS PROCESADAS</div>', unsafe_allow_html=True)

    search_q = st.text_input("🔍 Buscar en noticias...", placeholder="Rusia, misil, acuerdo, energía...")

    news_df = dff.copy()
    if search_q:
        mask_s = (
            news_df["title"].str.contains(search_q, case=False, na=False) |
            news_df["summary"].str.contains(search_q, case=False, na=False) |
            news_df["pais"].str.contains(search_q, case=False, na=False)
        )
        news_df = news_df[mask_s]

    news_df = news_df.sort_values("timestamp", ascending=False) if "timestamp" in news_df.columns else news_df

    st.markdown(f'<div class="info-box">Mostrando <b>{len(news_df)}</b> eventos</div>', unsafe_allow_html=True)

    cols_n = ["timestamp", "pais", "title", "summary", "score", "source"]
    cols_n = [c for c in cols_n if c in news_df.columns]
    st.dataframe(news_df[cols_n], width="stretch", hide_index=True)

    st.markdown('<div class="section-title">DISTRIBUCIÓN POR FUENTE</div>', unsafe_allow_html=True)
    if "source" in dff.columns:
        src = dff["source"].value_counts().reset_index()
        src.columns = ["source", "count"]
        fig_src = go.Figure(go.Pie(
            labels=src["source"], values=src["count"],
            hole=0.55,
            marker=dict(colors=["#00ff41","#00cc33","#009922","#006611","#004411","#ffa500"]),
            textfont=dict(family="Courier New", size=10, color="#c8ffc8"),
        ))
        fig_src.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c8ffc8", family="Courier New"),
            legend=dict(bgcolor="rgba(15,26,15,0.7)", bordercolor="#1a3a1a"),
            margin=dict(l=0, r=0, t=20, b=0), height=320,
        )
        st.plotly_chart(fig_src, width="stretch")


# ── TAB 6 — TENDENCIAS ────────────────────────────────────────
with tabs[5]:
    st.markdown('<div class="section-title">TENDENCIAS TEMPORALES</div>', unsafe_allow_html=True)

    if "timestamp" in dff.columns and dff["timestamp"].notna().any():
        time_df = dff.dropna(subset=["timestamp"]).copy()
        time_df["date"] = time_df["timestamp"].dt.date

        daily = time_df.groupby("date").agg(
            score=("score", "sum"),
            eventos=("score", "count"),
        ).reset_index()

        fig_time = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                  vertical_spacing=0.05, row_heights=[0.6, 0.4])
        fig_time.add_trace(go.Scatter(
            x=daily["date"], y=daily["score"],
            mode="lines+markers",
            line=dict(color="#ff4040", width=2),
            marker=dict(color="#ff4040", size=5),
            name="Score diario",
            fill="tozeroy", fillcolor="rgba(255,64,64,0.08)",
        ), row=1, col=1)
        fig_time.add_trace(go.Bar(
            x=daily["date"], y=daily["eventos"],
            marker_color="rgba(0,255,65,0.4)",
            name="Eventos",
        ), row=2, col=1)

        fig_time.update_layout(
            **_layout,
            xaxis2=dict(showgrid=False, gridcolor="#1a3a1a"),
            margin=dict(l=0, r=0, t=20, b=20), height=480,
        )
        st.plotly_chart(fig_time, width="stretch")

        if "categoria" in dff.columns:
            st.markdown('<div class="section-title">EVOLUCIÓN POR CATEGORÍA</div>', unsafe_allow_html=True)
            cat_time = time_df.groupby(["date", "categoria"])["score"].sum().reset_index()
            fig_cat = px.area(cat_time, x="date", y="score", color="categoria",
                              color_discrete_sequence=["#00ff41","#00cc33","#ffa500","#ff4040","#4a7a4a"])
            fig_cat.update_layout(
                **_layout,
                margin=dict(l=0, r=0, t=20, b=20), height=300,
            )
            st.plotly_chart(fig_cat, width="stretch")
    else:
        st.markdown('<div class="alert-box">⚠ No hay datos temporales disponibles</div>', unsafe_allow_html=True)


# ── TAB 7 — METODOLOGÍA ───────────────────────────────────────
with tabs[6]:
    st.markdown('<div class="section-title">METODOLOGÍA & ARQUITECTURA SIEG</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""
<div class="info-box">
<b style="color:#00ff41;letter-spacing:0.1rem;">PIPELINE DE DATOS</b><br><br>
<span style="font-size:0.78rem;line-height:2;">
1. <b>Scraper</b> → RSS feeds, GDELT, ACLED<br>
2. <b>Processor</b> → NLP (RoBERTa-es), scoring<br>
3. <b>Score</b> = intensidad × frecuencia × relevancia<br>
4. <b>Cron</b> → cada hora (:55)<br>
5. <b>Almacenamiento</b> → CSV + logs rotados<br>
6. <b>Dashboard</b> → Streamlit (tiempo real)
</span>
</div>
""", unsafe_allow_html=True)

    with m2:
        st.markdown("""
<div class="info-box">
<b style="color:#00ff41;letter-spacing:0.1rem;">ÍNDICE DE RIESGO</b><br><br>
<span style="font-size:0.78rem;line-height:2;">
🔴 <b>CRÍTICO</b>  → Score ≥ 10<br>
🟠 <b>ALTO</b>     → Score ≥ 7<br>
🟡 <b>MEDIO</b>    → Score ≥ 4<br>
🟢 <b>BAJO</b>     → Score &lt; 4<br><br>
Score energético = score_conflicto × relevancia_geo
</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-box" style="margin-top:1rem;">
<b style="color:#00ff41;letter-spacing:0.1rem;">FUENTES DE DATOS</b><br><br>
<span style="font-size:0.8rem;line-height:2;">
Reuters · BBC World · Al Jazeera · AP · EFE · DW ·
GDELT Project · ACLED · Crisis Group · ReliefWeb ·
UN OCHA · SIPRI · Global Conflict Tracker (CFR)
</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-box" style="margin-top:1rem;">
<b style="color:#00ff41;letter-spacing:0.1rem;">DIMENSIONES DE ANÁLISIS</b><br><br>
<span style="font-size:0.8rem;line-height:2;">
+ <b>Militar</b>: combates activos, bajas, armamento<br>
+ <b>Diplomático</b>: sanciones, alianzas, tratados<br>
+ <b>Energético</b>: petróleo, gas, infraestructura crítica<br>
+ <b>Humanitario</b>: desplazados, crisis alimentaria<br>
+ <b>Cibernético</b>: ataques, desinformación, hacktivismo<br>
+ <b>Económico</b>: embargos, bloqueos, deuda soberana
</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="alert-box" style="margin-top:1.5rem;">
⚠ AVISO LEGAL: Dashboard de análisis informativo automatizado.
No constituye asesoramiento político ni militar. Datos de fuentes abiertas (OSINT).
El score de riesgo es un indicador algorítmico, no una evaluación oficial.
</div>
""", unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────
st.markdown(
    f"""
<div class="sieg-footer">
  SIEG · SISTEMA DE INTELIGENCIA ESTRATÉGICA GLOBAL — MÓDULO DE CONFLICTOS &nbsp;·&nbsp;
  © {NOW.year} M. Castillo &nbsp;·&nbsp; mybloogingnotes@gmail.com &nbsp;·&nbsp;
  <a href="https://github.com/mcasrom/sieg-conflicts" style="color:#00cc33;text-decoration:none">
    github.com/mcasrom/sieg-conflicts
  </a> &nbsp;·&nbsp;
  Datos actualizados: {NOW.strftime('%Y-%m-%d %H:%M UTC')}
</div>
""",
    unsafe_allow_html=True,
)
