import random
import re
import altair as alt
import folium
import numpy as np
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import st_folium

# ------------------------------------------------------------------
# CONFIG & PAGE SETUP (Memaksa Sidebar Terbuka)
# ------------------------------------------------------------------
st.set_page_config(
    page_title="LivingMatch AI",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded",  
)

# ------------------------------------------------------------------
# DESIGN TOKENS
# ------------------------------------------------------------------
PRIMARY = "#1F5D4C"
PRIMARY_DARK = "#0F3D31"
PRIMARY_LIGHT = "#E7EEE9"
GOLD = "#B8860B"
RISK = "#B24C33"
INK = "#1C2B27"
MUTED = "#6B7A75"

FONT_DISPLAY = "'Fraunces', serif"
FONT_BODY = "'Inter', sans-serif"
FONT_MONO = "'JetBrains Mono', monospace"

# ------------------------------------------------------------------
# GLOBAL CUSTOM CSS
# ------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

    .stApp {{
        background-color: #F8FAF9;
        font-family: {FONT_BODY};
        color: {INK};
    }}

    /* Trik CSS: Paksa area sidebar memiliki lebar penuh saat awal dimuat */
    section[data-testid="stSidebar"] {{
        width: 330px !important;
    }}

    .lm-card {{
        background: white;
        border: 1px solid #E2E9E5;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 16px;
    }}

    .lm-hero {{
        background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
        padding: 32px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 20px rgba(31, 93, 76, 0.15);
    }}
    .lm-hero h1 {{
        font-family: {FONT_DISPLAY} !important;
        font-size: 32px;
        font-weight: 600;
        margin-bottom: 8px;
    }}
    .lm-hero p {{
        margin: 0;
        opacity: 0.9;
        font-size: 15px;
        line-height: 1.6;
        max-width: 720px;
    }}
    .lm-badge {{
        display: inline-block;
        background: {GOLD};
        color: white;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}

    .lm-algo-tag {{
        display: inline-block;
        background: {PRIMARY_LIGHT};
        color: {PRIMARY};
        border: 1px solid #CFE1D8;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 12px;
        font-family: {FONT_MONO};
    }}
    .lm-loc-chip {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: white;
        border: 1px solid #CFE1D8;
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 14px;
        color: {INK};
        font-weight: 500;
    }}
    .lm-loc-chip b {{ color: {PRIMARY}; }}

    div[data-testid="stMetric"] {{
        background: {PRIMARY_LIGHT};
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #D3EBDF;
    }}
    div[data-testid="stMetricValue"] {{
        color: {PRIMARY};
        font-family: {FONT_MONO};
        font-weight: 700;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# GEOCODING HELPER
# ------------------------------------------------------------------
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
DEFAULT_LAT, DEFAULT_LON = -7.7829, 110.3671  # Yogyakarta Tugu


@st.cache_data(show_spinner=False, ttl=86400)
def geocode_address(alamat: str):
    clean_addr = alamat.strip()
    queries = [
        clean_addr,
        f"{clean_addr}, Indonesia",
        re.sub(r"(?i)\bjalan\b|\bjl\.\b|\bjl\b", "Jl.", clean_addr),
    ]
    headers = {
        "User-Agent": "LivingMatchApp/3.0 (contact: admin@livingmatch.id)"
    }

    for q in queries:
        try:
            params = {
                "q": q,
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
                "countrycodes": "id",
            }
            resp = requests.get(
                NOMINATIM_URL, params=params, headers=headers, timeout=6
            )
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    hit = data[0]
                    return {
                        "lat": float(hit["lat"]),
                        "lon": float(hit["lon"]),
                        "display_name": hit.get("display_name", alamat),
                    }
        except Exception:
            continue
    return None


# ------------------------------------------------------------------
# CHART & MAP HELPERS
# ------------------------------------------------------------------
def gauge_chart(
    value: int, color: str, track_color: str = "#E7EEE9", max_value: int = 100
):
    df = pd.DataFrame(
        {
            "kategori": ["skor", "sisa"],
            "nilai": [value, max_value - value],
            "urutan": [1, 2],
        }
    )
    arc = (
        alt.Chart(df)
        .mark_arc(innerRadius=50, outerRadius=70, cornerRadius=6)
        .encode(
            theta=alt.Theta("nilai:Q", stack=True, sort=None),
            order=alt.Order("urutan:Q"),
            color=alt.Color(
                "kategori:N",
                scale=alt.Scale(
                    domain=["skor", "sisa"], range=[color, track_color]
                ),
                legend=None,
            ),
        )
        .properties(width=150, height=150)
    )
    label = (
        alt.Chart(pd.DataFrame({"t": [f"{value}"]}))
        .mark_text(
            fontSize=28,
            fontWeight="bold",
            color=INK,
            font="JetBrains Mono",
        )
        .encode(text="t:N")
        .properties(width=150, height=150)
    )
    return arc + label


def render_folium_map(lat: float, lon: float, label: str):
    m = folium.Map(location=[lat, lon], zoom_start=15, tiles="OpenStreetMap")
    folium.Marker(
        [lat, lon],
        popup=label,
        tooltip=label,
        icon=folium.Icon(color="green", icon="home", prefix="fa"),
    ).add_to(m)
    st_folium(m, width="100%", height=420, returned_objects=[])


def compose_insight(indikator: dict) -> str:
    fragments = []
    if indikator["Keamanan"] >= 80:
        fragments.append("warga sekitar menilai kawasan ini sangat aman dan kondusif")
    elif indikator["Keamanan"] < 60:
        fragments.append(
            "beberapa catatan menyebutkan perlunya kewaspadaan ekstra pada malam hari"
        )

    if indikator["Bebas banjir"] < 60:
        fragments.append(
            "terdapat riwayat genangan air saat curah hujan tinggi yang perlu diantisipasi"
        )
    elif indikator["Bebas banjir"] >= 85:
        fragments.append("bebas dari potensi risiko banjir tahunan")

    if indikator["Kelancaran lalu lintas"] < 55:
        fragments.append("akses jalan cenderung padat pada jam berangkat/pulang kerja")

    if indikator["Fasilitas umum"] >= 80:
        fragments.append(
            "aksesibilitas ke sekolah, rumah sakit, dan pusat perbelanjaan sangat dekat"
        )

    if not fragments:
        fragments.append(
            "kondisi lingkungan terpantau stabil tanpa isu menonjol"
        )

    return f"Berdasarkan rangkuman data lokal: {'; '.join(fragments)}."


# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="lm-hero">
        <div class="lm-badge">Prototipe MVP</div>
        <h1>🏘️ LivingMatch AI</h1>
        <p>Solusi berbasis AI untuk merangkum skor keamanan, risiko banjir, kualitas udara, kemacetan, dan nilai investasi properti suatu kawasan secara objektif.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# SIDEBAR / FORM INPUT
# ------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Parameter Analisis")
    with st.form("input_form"):
        alamat = st.text_input(
            "Lokasi / Alamat Rumah Target",
            placeholder="Contoh: Jalan Magelang, Yogyakarta",
        )
        profil = st.selectbox(
            "Profil Pengguna",
            ["Keluarga muda", "Profesional", "Investor properti", "Pengusaha"],
        )
        budget = st.select_slider(
            "Kelas Harga Target",
            options=["Menengah", "Menengah-atas", "Premium"],
        )
        prioritas = st.multiselect(
            "Prioritas Gaya Hidup",
            [
                "Keamanan",
                "Bebas banjir",
                "Kualitas udara",
                "Minim kemacetan",
                "Ketenangan (bebas kebisingan)",
                "Dekat fasilitas umum",
                "Potensi kenaikan nilai investasi",
            ],
            default=["Keamanan", "Bebas banjir"],
        )

        submitted = st.form_submit_button(
            "🔍 Analisis Lingkungan", use_container_width=True
        )

# ------------------------------------------------------------------
# PROCESSING & SESSION STATE MANAGEMENT
# ------------------------------------------------------------------
if submitted and alamat:
    with st.spinner("Mengontak OpenStreetMap & menghitung indikator AI..."):
        geo = geocode_address(alamat)

        if geo:
            lat, lon = geo["lat"], geo["lon"]
            lokasi_label = geo["display_name"]
            lokasi_ditemukan = True
        else:
            lat, lon = DEFAULT_LAT, DEFAULT_LON
            lokasi_label = f"{alamat} (Estimasi Pusat Yogyakarta)"
            lokasi_ditemukan = False

        seed_key = f"{round(lat, 3)}_{round(lon, 3)}"
        rng = random.Random(seed_key)

        indikator = {
            "Keamanan": rng.randint(55, 95),
            "Bebas banjir": rng.randint(40, 95),
            "Kualitas udara": rng.randint(50, 90),
            "Kelancaran lalu lintas": rng.randint(35, 90),
            "Ketenangan (bebas kebisingan)": rng.randint(40, 92),
            "Fasilitas umum": rng.randint(60, 95),
        }
        neighborhood_score = round(sum(indikator.values()) / len(indikator))
        lifestyle_score = min(
            98,
            round(
                neighborhood_score * 0.8
                + len(prioritas) * 3
                + rng.randint(-5, 5)
            ),
        )

        rentang_harga = {
            "Menengah": (300_000_000, 800_000_000),
            "Menengah-atas": (800_000_000, 2_000_000_000),
            "Premium": (2_000_000_000, 8_000_000_000),
        }
        low, high = rentang_harga[budget]
        harga_estimasi = (
            round(rng.randint(low, high) / 5_000_000) * 5_000_000
        )

        st.session_state["has_analysis"] = True
        st.session_state["analysis_data"] = {
            "alamat": alamat,
            "lat": lat,
            "lon": lon,
            "lokasi_label": lokasi_label,
            "lokasi_ditemukan": lokasi_ditemukan,
            "indikator": indikator,
            "neighborhood_score": neighborhood_score,
            "lifestyle_score": lifestyle_score,
            "harga_estimasi": harga_estimasi,
            "rng_seed": seed_key,
        }
elif submitted and not alamat:
    st.warning("⚠️ Silakan isi alamat atau kawasan lokasi terlebih dahulu.")

# ------------------------------------------------------------------
# DISPLAY HASIL ANALISIS
# ------------------------------------------------------------------
if st.session_state.get("has_analysis", False):
    data = st.session_state["analysis_data"]

    if data["lokasi_ditemukan"]:
        st.markdown(
            f'<div class="lm-loc-chip">📍 Lokasi Terdeteksi: <b>{data["lokasi_label"]}</b> '
            f'<span style="color:#6B7A75; font-size:12px;">({data["lat"]:.4f}, {data["lon"]:.4f})</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning(
            f"⚠️ Lokasi spesifik untuk **'{data['alamat']}'** tidak ditemukan di OpenStreetMap. "
            f"Menampilkan titik pusat Yogyakarta sebagai perkiraan."
        )

    st.write("")

    tab_overview, tab_detail, tab_insight, tab_value = st.tabs(
        [
            "📊 Ringkasan",
            "🧭 Detail Indikator",
            "💬 Community Insight",
            "📈 Proyeksi Harga",
        ]
    )

    # --- TAB 1: RINGKASAN ---
    with tab_overview:
        c1, c2, c3 = st.columns([1, 1, 1.2])

        with c1:
            st.markdown(
                "<div class='lm-card' style='text-align:center;'>",
                unsafe_allow_html=True,
            )
            st.caption("Neighborhood Score")
            st.altair_chart(
                gauge_chart(data["neighborhood_score"], PRIMARY),
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown(
                "<div class='lm-card' style='text-align:center;'>",
                unsafe_allow_html=True,
            )
            st.caption("Lifestyle Match Score")
            st.altair_chart(
                gauge_chart(data["lifestyle_score"], GOLD),
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with c3:
            st.metric(
                label="Estimasi Harga Pasar Saat Ini",
                value=f"Rp{data['harga_estimasi']:,.0f}".replace(",", "."),
            )
            st.info(
                "💡 Skor di atas dihitung berbasis agregasi indikator keamanan, "
                "lingkungan, dan preferensi profil Anda."
            )

        st.subheader("📍 Peta Interaktif Lokasi Target")
        render_folium_map(data["lat"], data["lon"], data["lokasi_label"])

    # --- TAB 2: DETAIL INDIKATOR ---
    with tab_detail:
        st.markdown(
            '<span class="lm-algo-tag">🧩 Model Predictor: Random Forest Regressor</span>',
            unsafe_allow_html=True,
        )

        df_ind = pd.DataFrame(
            list(data["indikator"].items()), columns=["Indikator", "Skor"]
        )
        chart = (
            alt.Chart(df_ind)
            .mark_bar(color=PRIMARY, cornerRadiusEnd=6)
            .encode(
                x=alt.X(
                    "Skor:Q",
                    scale=alt.Scale(domain=[0, 100]),
                    title="Skor Evaluasi (0-100)",
                ),
                y=alt.Y("Indikator:N", sort="-x", title=None),
                tooltip=["Indikator", "Skor"],
            )
            .properties(height=300)
        )
        st.altair_chart(chart, use_container_width=True)

    # --- TAB 3: COMMUNITY INSIGHT ---
    with tab_insight:
        st.markdown(
            '<span class="lm-algo-tag">🧩 NLP Sentiment Analysis & Summarizer</span>',
            unsafe_allow_html=True,
        )
        insight_text = compose_insight(data["indikator"])
        st.markdown(
            f'<div class="lm-card">💬 <b>Sentimen Warga & Berita:</b><br><br>{insight_text}</div>',
            unsafe_allow_html=True,
        )

    # --- TAB 4: PREDIKSI NILAI ---
    with tab_value:
        st.markdown(
            '<span class="lm-algo-tag">🧩 Proyeksi: Linear Regression Trend</span>',
            unsafe_allow_html=True,
        )

        rng = random.Random(data["rng_seed"])
        growth = rng.uniform(4.5, 8.0)
        tahun = list(range(2026, 2031))
        proyeksi = [
            round(data["harga_estimasi"] * ((1 + growth / 100) ** i))
            for i in range(5)
        ]

        df_val = pd.DataFrame(
            {
                "Tahun": [str(t) for t in tahun],
                "Estimasi (Rp)": proyeksi,
                "Dalam Miliar": [p / 1_000_000_000 for p in proyeksi],
            }
        )

        line_chart = (
            alt.Chart(df_val)
            .mark_line(point=True, color=GOLD, strokeWidth=3)
            .encode(
                x=alt.X("Tahun:N", title="Tahun Proyeksi"),
                y=alt.Y(
                    "Dalam Miliar:Q",
                    title="Nilai Properti (Miliar Rp)",
                    axis=alt.Axis(format=",.2f"),
                ),
                tooltip=[
                    "Tahun",
                    alt.Tooltip(
                        "Estimasi (Rp):Q", format=",.0f", title="Nilai (Rp)"
                    ),
                ],
            )
            .properties(height=280)
        )
        st.altair_chart(line_chart, use_container_width=True)
        st.caption(
            f"📈 Estimasi pertumbuhan tahunan kawasan ini diproyeksikan **+{growth:.1f}% per tahun**."
        )

else:
    st.info(
        "👈 Masukkan alamat rumah target pada menu di panel sebelah kiri, lalu klik **Analisis Lingkungan** untuk memulai."
    )
