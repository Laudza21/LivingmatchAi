import random

import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import requests
import streamlit as st

st.set_page_config(page_title="LivingMatch AI", page_icon="🏘️", layout="centered")

# ------------------------------------------------------------------
# DESIGN TOKENS
# ------------------------------------------------------------------
# Warna mengikuti .streamlit/config.toml (identitas "trust & finansial"):
PRIMARY = "#1F5D4C"        # hijau tua — kepercayaan, lingkungan
PRIMARY_DARK = "#0F3D31"
PRIMARY_LIGHT = "#E7EEE9"  # secondaryBackgroundColor
GOLD = "#B8860B"           # aksen investasi/nilai
RISK = "#B24C33"           # terracotta redup — dipakai HANYA untuk sinyal risiko, jangan dekoratif
INK = "#1C2B27"            # textColor
MUTED = "#6B7A75"

FONT_DISPLAY = "'Fraunces', serif"
FONT_BODY = "'Inter', sans-serif"
FONT_MONO = "'JetBrains Mono', monospace"

# ------------------------------------------------------------------
# GLOBAL STYLES
# ------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

    .stApp {{
        background-color: #F4F7F5;
        font-family: {FONT_BODY};
        color: {INK};
    }}

    h1, h2, h3, .lm-hero h1, .lm-section-title {{
        font-family: {FONT_DISPLAY} !important;
    }}

    .lm-mono {{
        font-family: {FONT_MONO};
        font-variant-numeric: tabular-nums;
    }}

    /* Hero */
    .lm-hero {{
        background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
        padding: 30px 30px 26px 30px;
        border-radius: 18px;
        color: white;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }}
    .lm-hero::after {{
        content: "";
        position: absolute;
        right: -40px; top: -40px;
        width: 160px; height: 160px;
        border-radius: 50%;
        background: rgba(184,134,11,0.18);
    }}
    .lm-hero h1 {{
        margin: 0;
        font-size: 30px;
        font-weight: 600;
        letter-spacing: -0.01em;
    }}
    .lm-hero p {{
        margin: 8px 0 0 0;
        opacity: 0.88;
        font-size: 14.5px;
        line-height: 1.55;
        max-width: 640px;
        position: relative;
        z-index: 1;
    }}
    .lm-badge {{
        display: inline-block;
        background: {GOLD};
        color: white;
        padding: 3px 11px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 12px;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }}

    .lm-card {{
        background: white;
        border: 1px solid #DFE7E2;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 14px;
    }}
    .lm-section-title {{
        font-size: 19px;
        font-weight: 600;
        color: {INK};
        margin-bottom: 2px;
    }}
    .lm-section-sub {{
        font-size: 13px;
        color: {MUTED};
        margin-bottom: 10px;
    }}
    .lm-algo-tag {{
        display: inline-block;
        background: {PRIMARY_LIGHT};
        color: {PRIMARY};
        border: 1px solid #CFE1D8;
        padding: 3px 11px;
        border-radius: 999px;
        font-size: 11.5px;
        font-weight: 600;
        margin-bottom: 12px;
        font-family: {FONT_MONO};
    }}
    .lm-loc-chip {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: white;
        border: 1px solid #DFE7E2;
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 13px;
        color: {INK};
        margin: 10px 0 4px 0;
    }}
    .lm-loc-chip b {{ color: {PRIMARY}; }}
    .lm-coord {{
        font-family: {FONT_MONO};
        font-size: 11.5px;
        color: {MUTED};
    }}

    div[data-testid="stMetric"] {{
        background: {PRIMARY_LIGHT};
        border-radius: 12px;
        padding: 14px 16px;
        border: 1px solid #D3EBDF;
    }}
    div[data-testid="stMetricValue"] {{
        color: {PRIMARY};
        font-family: {FONT_MONO};
    }}

    .stButton>button {{
        background-color: {PRIMARY};
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 18px;
        font-weight: 600;
    }}
    .stButton>button:hover {{
        background-color: {PRIMARY_DARK};
        color: white;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        font-weight: 600;
        color: {MUTED};
    }}
    .stTabs [aria-selected="true"] {{
        color: {PRIMARY} !important;
        border-bottom: 3px solid {GOLD} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# HERO HEADER
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="lm-hero">
        <div class="lm-badge">Prototipe MVP · Kewirausahaan Syariah</div>
        <h1>🏘️ LivingMatch AI</h1>
        <p>"Skor kredit untuk lingkungan rumah" — merangkum keamanan, risiko banjir, kualitas
        udara, kemacetan, kebisingan, dan aksesibilitas fasilitas umum suatu kawasan menjadi
        satu penilaian yang objektif, sebelum kamu memutuskan membeli atau berinvestasi.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "**Catatan prototipe (MVP):** skor lingkungan & estimasi harga di bawah dihasilkan dari "
    "simulasi berbasis aturan (rule-based), bukan model Machine Learning yang sudah dilatih "
    "dengan data riil — merepresentasikan bentuk output dari Random Forest, KNN, NLP+Naive "
    "Bayes+LLM, dan Linear Regression pada versi produksi. **Titik lokasi di peta bersifat "
    "nyata**, diambil dari layanan geocoding terbuka OpenStreetMap (Nominatim), bukan simulasi."
)

# ------------------------------------------------------------------
# GEOCODING (DATA NYATA — OpenStreetMap Nominatim, gratis tanpa API key)
# ------------------------------------------------------------------
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
DEFAULT_LAT, DEFAULT_LON = -7.7956, 110.3695  # fallback: pusat Yogyakarta


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def geocode_address(alamat: str):
    """Ambil koordinat & nama lokasi yang dikenali dari OpenStreetMap Nominatim.

    Gratis dan tanpa API key, tapi wajib kirim User-Agent unik sesuai kebijakan
    penggunaan Nominatim (https://operations.osmfoundation.org/policies/nominatim/).
    Mengembalikan None jika lokasi tidak ditemukan atau layanan tidak terjangkau.
    """
    try:
        resp = requests.get(
            NOMINATIM_URL,
            params={
                "q": alamat if "indonesia" in alamat.lower() else f"{alamat}, Indonesia",
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
            },
            headers={"User-Agent": "LivingMatchAI-MVP/1.0 (tugas-kuliah; contact: livingmatch@example.com)"},
            timeout=6,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        hit = data[0]
        return {
            "lat": float(hit["lat"]),
            "lon": float(hit["lon"]),
            "display_name": hit.get("display_name", alamat),
        }
    except Exception:
        return None


# ------------------------------------------------------------------
# CHART HELPERS
# ------------------------------------------------------------------
def gauge_chart(value: int, color: str, track_color: str = "#E7EEE9", max_value: int = 100):
    """Donut gauge ala 'skor kredit' dengan angka besar di tengah."""
    df = pd.DataFrame(
        {
            "kategori": ["skor", "sisa"],
            "nilai": [value, max_value - value],
            "urutan": [1, 2],
        }
    )
    arc = (
        alt.Chart(df)
        .mark_arc(innerRadius=54, outerRadius=76, cornerRadius=8)
        .encode(
            theta=alt.Theta("nilai:Q", stack=True, sort=None),
            order=alt.Order("urutan:Q"),
            color=alt.Color(
                "kategori:N",
                scale=alt.Scale(domain=["skor", "sisa"], range=[color, track_color]),
                legend=None,
            ),
        )
        .properties(width=170, height=170)
    )
    label = (
        alt.Chart(pd.DataFrame({"t": [f"{value}"]}))
        .mark_text(fontSize=32, fontWeight="bold", color=INK, font="JetBrains Mono")
        .encode(text="t:N")
        .properties(width=170, height=170)
    )
    return arc + label


def render_map(lat: float, lon: float, label: str):
    df_map = pd.DataFrame({"lat": [lat], "lon": [lon], "label": [label]})
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_map,
        get_position="[lon, lat]",
        get_fill_color="[184, 134, 11, 210]",
        get_line_color="[15, 61, 49, 255]",
        line_width_min_pixels=2,
        get_radius=110,
        radius_min_pixels=9,
        radius_max_pixels=22,
        stroked=True,
        pickable=True,
    )
    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=13.5, pitch=0)
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=None,  # basemap gratis bawaan pydeck, tanpa perlu token Mapbox
        tooltip={"text": "{label}"},
    )
    st.pydeck_chart(deck, use_container_width=True)


def compose_insight(indikator: dict) -> str:
    """Rangkai narasi Community Insight dari kombinasi indikator individual —
    mensimulasikan bentuk output NLP + Naive Bayes + ringkasan LLM tanpa
    memerlukan data ulasan/berita riil."""
    fragments = []

    if indikator["Keamanan"] >= 80:
        fragments.append("warga sekitar menilai kawasan ini relatif aman dan tertata")
    elif indikator["Keamanan"] < 60:
        fragments.append("sejumlah ulasan menyoroti kekhawatiran keamanan pada jam-jam tertentu")

    if indikator["Bebas banjir"] < 60:
        fragments.append("ada catatan riwayat genangan air saat musim hujan yang sebaiknya dikonfirmasi langsung")
    elif indikator["Bebas banjir"] >= 85:
        fragments.append("kawasan ini jarang dilaporkan mengalami genangan air signifikan")

    if indikator["Kelancaran lalu lintas"] < 55:
        fragments.append("kemacetan pada jam sibuk cukup sering muncul dalam ulasan warga")

    if indikator["Ketenangan (bebas kebisingan)"] < 55:
        fragments.append("tingkat kebisingan di area ini tergolong tinggi menurut sejumlah laporan")

    if indikator["Fasilitas umum"] >= 80:
        fragments.append("aksesibilitas ke fasilitas umum dinilai sangat memadai")

    if not fragments:
        fragments.append("belum ada pola sentimen yang menonjol dari data yang tersedia")

    narasi = "; ".join(fragments)
    return f"Berdasarkan simulasi rangkuman ulasan & pemberitaan lokal: {narasi}."


# ------------------------------------------------------------------
# FORM
# ------------------------------------------------------------------
st.markdown('<div class="lm-section-title">1. Lokasi & preferensi</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="lm-section-sub">Masukkan rumah yang sedang kamu incar — AI yang akan '
    "memperkirakan kondisi lingkungan dan estimasi harganya, kamu tidak perlu tahu angkanya duluan.</div>",
    unsafe_allow_html=True,
)

with st.form("input_form"):
    alamat = st.text_input(
        "Alamat atau kawasan rumah yang diincar",
        placeholder="Contoh: Jl. Kaliurang KM 10, Sleman",
    )

    col1, col2 = st.columns(2)
    with col1:
        profil = st.selectbox(
            "Profil pengguna",
            ["Keluarga muda", "Profesional", "Investor properti", "Pengusaha"],
        )
    with col2:
        budget = st.select_slider(
            "Kelas harga rumah yang dicari",
            options=["Menengah", "Menengah-atas", "Premium"],
            help="Dipakai AI sebagai konteks kisaran pasar saat memperkirakan harga kawasan ini.",
        )

    prioritas = st.multiselect(
        "Prioritas gaya hidup (pilih yang paling penting)",
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

    submitted = st.form_submit_button("🔍 Analisis lingkungan")

if submitted and not alamat:
    st.warning("Isi dulu alamat atau kawasan yang mau dianalisis.")

if submitted and alamat:
    with st.spinner("Mencari titik lokasi & menyusun analisis…"):
        geo = geocode_address(alamat)

    if geo:
        lat, lon = geo["lat"], geo["lon"]
        lokasi_label = geo["display_name"]
        seed_key = f"{round(lat, 3)}_{round(lon, 3)}"
        lokasi_ditemukan = True
    else:
        lat, lon = DEFAULT_LAT, DEFAULT_LON
        lokasi_label = alamat
        seed_key = alamat
        lokasi_ditemukan = False

    # Seed konsisten per lokasi (bukan per string mentah) supaya alamat yang
    # merujuk titik nyata sama akan menghasilkan skor yang sama.
    rng = random.Random(seed_key)

    # --- Simulasi Neighborhood Score (merepresentasikan output Random Forest) ---
    indikator = {
        "Keamanan": rng.randint(55, 95),
        "Bebas banjir": rng.randint(40, 95),
        "Kualitas udara": rng.randint(50, 90),
        "Kelancaran lalu lintas": rng.randint(35, 90),
        "Ketenangan (bebas kebisingan)": rng.randint(40, 92),
        "Fasilitas umum": rng.randint(60, 95),
    }
    neighborhood_score = round(sum(indikator.values()) / len(indikator))

    # --- Simulasi Lifestyle Match Score (merepresentasikan output KNN) ---
    bobot_prioritas = len(prioritas) if prioritas else 1
    lifestyle_score = min(
        98, round(neighborhood_score * 0.8 + bobot_prioritas * 3 + rng.randint(-5, 5))
    )

    # --- Simulasi estimasi harga pasar saat ini ---
    rentang_harga = {
        "Menengah": (300_000_000, 800_000_000),
        "Menengah-atas": (800_000_000, 2_000_000_000),
        "Premium": (2_000_000_000, 8_000_000_000),
    }
    low, high = rentang_harga[budget]
    harga_pasar_estimasi = round(rng.randint(low, high) / 5_000_000) * 5_000_000

    st.markdown("---")
    st.markdown('<div class="lm-section-title">2. Hasil analisis</div>', unsafe_allow_html=True)

    if lokasi_ditemukan:
        st.markdown(
            f'<div class="lm-loc-chip">📍 Lokasi teridentifikasi: <b>{lokasi_label}</b></div>'
            f'<div class="lm-coord">lat {lat:.5f}, lon {lon:.5f} · sumber: OpenStreetMap Nominatim</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="lm-loc-chip">📍 Menganalisis: <b>{alamat}</b></div>',
            unsafe_allow_html=True,
        )
        st.warning(
            "Titik persis tidak ditemukan di OpenStreetMap — peta menampilkan area terdekat "
            "sebagai perkiraan. Skor tetap dihitung berdasarkan teks alamat yang kamu masukkan. "
            "Coba tulis alamat yang lebih spesifik (nama jalan + kecamatan/kota) untuk hasil peta "
            "yang lebih presisi."
        )

    tab_overview, tab_detail, tab_insight, tab_value = st.tabs(
        ["📊 Ringkasan", "🧭 Detail Lingkungan", "💬 Community Insight", "📈 Prediksi Nilai"]
    )

    # ---------------- TAB 1: RINGKASAN ----------------
    with tab_overview:
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("**Neighborhood Score**")
            st.altair_chart(gauge_chart(neighborhood_score, PRIMARY), use_container_width=True)
        with g2:
            st.markdown("**Lifestyle Match Score**")
            st.altair_chart(gauge_chart(lifestyle_score, GOLD), use_container_width=True)

        st.metric("Estimasi Harga Pasar", f"Rp{harga_pasar_estimasi:,.0f}".replace(",", "."))

        st.markdown("**Titik lokasi**")
        render_map(lat, lon, lokasi_label)
        st.caption("Peta & koordinat bersumber dari OpenStreetMap Nominatim (data nyata, bukan simulasi).")

    # ---------------- TAB 2: DETAIL LINGKUNGAN ----------------
    with tab_detail:
        st.markdown(
            '<span class="lm-algo-tag">🧩 Simulasi output Random Forest</span>',
            unsafe_allow_html=True,
        )
        df_ind = pd.DataFrame(list(indikator.items()), columns=["Indikator", "Skor"])
        bar_chart = (
            alt.Chart(df_ind)
            .mark_bar(color=PRIMARY, cornerRadius=4)
            .encode(
                x=alt.X("Skor:Q", title="Skor (0–100)", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y("Indikator:N", sort="-x", title=None),
                tooltip=["Indikator", "Skor"],
            )
            .properties(height=250)
        )
        st.altair_chart(bar_chart, use_container_width=True)

    # ---------------- TAB 3: COMMUNITY INSIGHT ----------------
    with tab_insight:
        st.markdown(
            '<span class="lm-algo-tag">🧩 Simulasi output NLP + Naive Bayes + ringkasan LLM</span>',
            unsafe_allow_html=True,
        )
        insight = compose_insight(indikator)
        st.markdown(f'<div class="lm-card">💬 {insight}</div>', unsafe_allow_html=True)
        st.caption(
            "Pada versi produksi, narasi ini dihasilkan dari analisis sentimen ulasan Google Maps, "
            "berita lokal, dan forum warga — bukan disusun dari indikator numerik seperti pada "
            "prototipe ini."
        )

    # ---------------- TAB 4: PREDIKSI NILAI ----------------
    with tab_value:
        st.markdown(
            '<span class="lm-algo-tag">🧩 Simulasi output Linear Regression</span>',
            unsafe_allow_html=True,
        )
        growth = rng.uniform(3, 9)
        tahun = list(range(2026, 2031))
        proyeksi = [round(harga_pasar_estimasi * (1 + growth / 100) ** i) for i in range(5)]
        df_val = pd.DataFrame({"Tahun": tahun, "Estimasi harga (Rp)": proyeksi})
        df_val["Tahun"] = df_val["Tahun"].astype(str)

        line_chart = (
            alt.Chart(df_val)
            .mark_line(point=True, color=GOLD, strokeWidth=3)
            .encode(
                x=alt.X("Tahun:N", title="Tahun"),
                y=alt.Y(
                    "Estimasi harga (Rp):Q",
                    title="Estimasi harga rumah (Rp)",
                    axis=alt.Axis(format="~s"),
                    scale=alt.Scale(zero=False),
                ),
                tooltip=["Tahun", alt.Tooltip("Estimasi harga (Rp):Q", format=",.0f")],
            )
            .properties(height=260)
        )
        st.altair_chart(line_chart, use_container_width=True)
        st.caption(
            f"Titik tahun 2026 (Rp{harga_pasar_estimasi:,.0f}".replace(",", ".")
            + f") adalah estimasi harga pasar saat ini. Proyeksi memakai asumsi pertumbuhan "
            f"sekitar **{growth:.1f}% per tahun** berdasarkan tren infrastruktur & fasilitas sekitar."
        )

    st.success("Analisis selesai — skor & narasi di atas adalah simulasi untuk keperluan demo MVP; titik lokasi bersumber nyata dari OpenStreetMap.")

st.markdown("---")
st.caption("LivingMatch AI · Prototipe MVP · Jurusan Informatika, Universitas Islam Indonesia")
