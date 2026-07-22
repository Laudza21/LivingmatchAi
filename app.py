"""
LivingMatch AI — Prototipe MVP
Aplikasi Analisis Kualitas Lingkungan Berbasis AI untuk Keputusan Pembelian Rumah
Universitas Islam Indonesia — Jurusan Informatika
"""

import hashlib
import random
from datetime import datetime

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# ============================================================================
# KONFIGURASI HALAMAN
# ============================================================================
st.set_page_config(
    page_title="LivingMatch AI — Analisis Lingkungan Rumah",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# PALET WARNA & DESAIN
# ============================================================================
NAVY = "#0F2942"
NAVY_LIGHT = "#1B3A5C"
GOLD = "#C9A24B"
GOLD_LIGHT = "#E8D5A3"
CREAM = "#FAF7F0"
INK = "#1A1A1A"
MUTED = "#6B7280"
GREEN = "#2E7D5B"
AMBER = "#B8860B"
RED = "#B03A2E"

CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Source+Serif+4:wght@600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    .stApp {{
        background: linear-gradient(180deg, {CREAM} 0%, #FFFFFF 22%);
    }}

    /* Sembunyikan chrome bawaan Streamlit */
    #MainMenu, footer, header {{visibility: hidden;}}

    /* ---------- HERO HEADER ---------- */
    .lm-hero {{
        background: linear-gradient(120deg, {NAVY} 0%, {NAVY_LIGHT} 55%, {NAVY} 100%);
        border-radius: 18px;
        padding: 2.1rem 2.4rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 12px 30px rgba(15, 41, 66, 0.22);
        position: relative;
        overflow: hidden;
    }}
    .lm-hero::after {{
        content: "";
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, {GOLD}33 0%, transparent 70%);
    }}
    .lm-hero-eyebrow {{
        color: {GOLD_LIGHT};
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }}
    .lm-hero-title {{
        font-family: 'Source Serif 4', serif;
        color: #FFFFFF;
        font-size: 2.1rem;
        font-weight: 700;
        line-height: 1.2;
        margin: 0;
    }}
    .lm-hero-sub {{
        color: #C7D2DE;
        font-size: 0.95rem;
        margin-top: 0.55rem;
        max-width: 620px;
        line-height: 1.5;
    }}

    /* ---------- KARTU UMUM ---------- */
    .lm-card {{
        background: #FFFFFF;
        border: 1px solid #ECE7DA;
        border-radius: 14px;
        padding: 1.15rem 1.3rem;
        box-shadow: 0 2px 10px rgba(15, 41, 66, 0.05);
        margin-bottom: 0.9rem;
        color: {INK};
        font-size: 0.94rem;
        line-height: 1.6;
    }}

    .lm-section-title {{
        font-family: 'Source Serif 4', serif;
        font-weight: 700;
        font-size: 1.28rem;
        color: {NAVY};
        margin: 1.6rem 0 0.6rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    .lm-section-title .lm-step {{
        background: {NAVY};
        color: {GOLD_LIGHT};
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.15rem 0.55rem;
        border-radius: 20px;
        letter-spacing: 0.05em;
    }}

    /* ---------- TAG ALGORITMA ---------- */
    .lm-algo-tag {{
        display: inline-block;
        background: {GOLD}1A;
        color: {AMBER};
        border: 1px solid {GOLD}55;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.22rem 0.65rem;
        border-radius: 20px;
        letter-spacing: 0.02em;
        margin-bottom: 0.55rem;
    }}

    /* ---------- SCORE GAUGE CARD ---------- */
    .lm-score-card {{
        background: linear-gradient(160deg, #FFFFFF 0%, {CREAM} 100%);
        border: 1px solid #ECE7DA;
        border-radius: 16px;
        padding: 1.3rem 1.4rem 1.1rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(15, 41, 66, 0.06);
        height: 100%;
    }}
    .lm-score-label {{
        font-size: 0.8rem;
        color: {MUTED};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.3rem;
    }}
    .lm-score-value {{
        font-family: 'Source Serif 4', serif;
        font-size: 2.6rem;
        font-weight: 700;
        line-height: 1;
    }}
    .lm-score-max {{
        font-size: 1.05rem;
        color: {MUTED};
        font-weight: 500;
    }}
    .lm-badge {{
        display: inline-block;
        margin-top: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
    }}

    /* ---------- INDIKATOR MINI ---------- */
    .lm-indicator {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px dashed #E7E2D4;
        font-size: 0.9rem;
    }}
    .lm-indicator:last-child {{ border-bottom: none; }}
    .lm-indicator-name {{ color: {INK}; font-weight: 500; }}
    .lm-indicator-val {{ font-weight: 700; }}

    /* ---------- FOOTER ---------- */
    .lm-footer {{
        text-align: center;
        color: {MUTED};
        font-size: 0.8rem;
        padding: 1.4rem 0 0.6rem;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {NAVY};
    }}
    section[data-testid="stSidebar"] * {{
        color: #E9EEF3 !important;
    }}
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stTextInput label,
    section[data-testid="stSidebar"] .stRadio label {{
        color: #E9EEF3 !important;
        font-weight: 600;
    }}
    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF10;
    }}
    .stButton>button {{
        background: {GOLD};
        color: {NAVY};
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        width: 100%;
        transition: 0.15s ease;
    }}
    .stButton>button:hover {{
        background: {GOLD_LIGHT};
        color: {NAVY};
    }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================================
# UTILITAS SIMULASI (mereprentasikan output model ML sesungguhnya)
# ============================================================================
def seeded_rng(*parts) -> random.Random:
    """RNG deterministik berdasarkan input pengguna agar hasil konsisten
    untuk kombinasi input yang sama — mensimulasikan model yang stabil."""
    key = "|".join(str(p) for p in parts)
    seed = int(hashlib.sha256(key.encode()).hexdigest(), 16) % (10 ** 8)
    return random.Random(seed)


def clamp(v, lo=0, hi=100):
    return max(lo, min(hi, v))


def score_color(score: int) -> str:
    if score >= 80:
        return GREEN
    if score >= 60:
        return AMBER
    return RED


def score_badge(score: int) -> tuple[str, str]:
    if score >= 80:
        return "Sangat Direkomendasikan", f"{GREEN}22", GREEN
    if score >= 60:
        return "Cukup Direkomendasikan", f"{AMBER}22", AMBER
    return "Perlu Pertimbangan Lebih", f"{RED}22", RED


# ============================================================================
# SIDEBAR — INPUT PENGGUNA (Tahap 1: Input User)
# ============================================================================
with st.sidebar:
    st.markdown(
        f"<div style='font-family:Source Serif 4, serif; font-size:1.35rem; "
        f"font-weight:700; color:{GOLD_LIGHT}; margin-bottom:0.1rem;'>🏡 LivingMatch AI</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='font-size:0.82rem; color:#B7C4D1; margin-bottom:1.3rem;'>"
        "Skor kredit untuk lingkungan rumah</div>",
        unsafe_allow_html=True,
    )

    st.markdown("**📍 Lokasi Properti**")
    alamat = st.text_input(
        "Alamat / titik lokasi",
        value="Jl. Kaliurang KM 8, Sleman, Yogyakarta",
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**👤 Profil & Prioritas Gaya Hidup**")
    persona = st.selectbox(
        "Kategori pengguna",
        ["Keluarga Muda", "Profesional / Eksekutif", "Investor Properti", "Pengusaha"],
    )

    kelas_harga = st.select_slider(
        "Kelas harga properti",
        options=["Menengah", "Menengah Atas", "Premium", "Ultra Premium"],
        value="Menengah Atas",
    )

    harga_dasar_map = {
        "Menengah": 850_000_000,
        "Menengah Atas": 2_100_000_000,
        "Premium": 4_500_000_000,
        "Ultra Premium": 9_000_000_000,
    }

    st.markdown("Bobot prioritas *(1 = tidak penting, 5 = sangat penting)*")
    p_keamanan = st.slider("🔒 Keamanan lingkungan", 1, 5, 5)
    p_banjir = st.slider("🌊 Bebas risiko banjir", 1, 5, 4)
    p_fasum = st.slider("🏥 Akses fasilitas umum", 1, 5, 4)
    p_macet = st.slider("🚗 Kelancaran lalu lintas", 1, 5, 3)
    p_investasi = st.slider("📈 Potensi kenaikan nilai", 1, 5, 3)

    st.markdown("---")
    run = st.button("🔍 Jalankan Analisis LivingMatch")

    st.markdown(
        "<div style='font-size:0.72rem; color:#8797A6; margin-top:1rem; line-height:1.5;'>"
        "Prototipe MVP — hasil analisis di bawah ini adalah simulasi untuk keperluan "
        "demonstrasi model AI (Random Forest, KNN, NLP + LLM, Linear Regression).</div>",
        unsafe_allow_html=True,
    )

# ============================================================================
# HEADER UTAMA
# ============================================================================
st.markdown(
    f"""
    <div class="lm-hero">
        <div class="lm-hero-eyebrow">PROTOTIPE MVP · ANALISIS LINGKUNGAN BERBASIS AI</div>
        <div class="lm-hero-title">LivingMatch AI</div>
        <div class="lm-hero-sub">
            Temukan lingkungan yang cocok, bukan cuma rumah. LivingMatch AI merangkum
            keamanan, risiko banjir, kualitas udara, kemacetan, fasilitas umum, dan
            persepsi warga menjadi satu skor lingkungan yang objektif dan mudah dipahami.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not run:
    c1, c2, c3 = st.columns(3)
    highlight_cards = [
        ("🧭", "Neighborhood Score", "Random Forest merangkum 6 indikator kuantitatif lingkungan menjadi satu skor terpadu."),
        ("🎯", "Lifestyle Match Score", "KNN mencocokkan profil gaya hidupmu dengan karakteristik lingkungan yang paling relevan."),
        ("💬", "Community Insight", "NLP + LLM merangkum ulasan warga, berita lokal, dan media sosial jadi satu narasi ringkas."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3], highlight_cards):
        with col:
            st.markdown(
                f"""<div class="lm-card" style="min-height:150px;">
                <div style="font-size:1.6rem;">{icon}</div>
                <div style="font-weight:700; color:{NAVY}; margin:0.35rem 0;">{title}</div>
                <div style="color:{MUTED}; font-size:0.86rem;">{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )
    st.info("👈 Masukkan alamat properti dan atur prioritas gaya hidupmu di sidebar, lalu klik **Jalankan Analisis LivingMatch** untuk melihat hasilnya.")
    st.markdown(
        f"<div class='lm-footer'>LivingMatch AI — Prototipe MVP · Proyek Kewirausahaan · "
        f"Jurusan Informatika, Universitas Islam Indonesia</div>",
        unsafe_allow_html=True,
    )
    st.stop()

# ============================================================================
# ENGINE SIMULASI (Tahap 2: Proses API & Engine AI)
# ============================================================================
rng = seeded_rng(alamat, persona, kelas_harga, p_keamanan, p_banjir, p_fasum, p_macet, p_investasi)

indikator = {
    "Keamanan / Kriminalitas": clamp(round(rng.gauss(72, 12))),
    "Risiko Banjir (semakin tinggi = semakin aman)": clamp(round(rng.gauss(68, 15))),
    "Kualitas Udara": clamp(round(rng.gauss(75, 10))),
    "Kelancaran Lalu Lintas": clamp(round(rng.gauss(60, 14))),
    "Ketenangan / Tingkat Kebisingan": clamp(round(rng.gauss(70, 11))),
    "Aksesibilitas Fasilitas Umum": clamp(round(rng.gauss(78, 9))),
}

bobot = {
    "Keamanan / Kriminalitas": p_keamanan,
    "Risiko Banjir (semakin tinggi = semakin aman)": p_banjir,
    "Kualitas Udara": 2,
    "Kelancaran Lalu Lintas": p_macet,
    "Ketenangan / Tingkat Kebisingan": 2,
    "Aksesibilitas Fasilitas Umum": p_fasum,
}

total_bobot = sum(bobot.values())
neighborhood_score = clamp(round(sum(indikator[k] * bobot[k] for k in indikator) / total_bobot))

persona_fit_base = {
    "Keluarga Muda": (indikator["Keamanan / Kriminalitas"] + indikator["Aksesibilitas Fasilitas Umum"]) / 2,
    "Profesional / Eksekutif": (indikator["Kelancaran Lalu Lintas"] + indikator["Ketenangan / Tingkat Kebisingan"]) / 2,
    "Investor Properti": (indikator["Aksesibilitas Fasilitas Umum"] + p_investasi * 14) / 2,
    "Pengusaha": (indikator["Kelancaran Lalu Lintas"] + indikator["Aksesibilitas Fasilitas Umum"]) / 2,
}
lifestyle_match = clamp(round(persona_fit_base[persona] * 0.7 + neighborhood_score * 0.3 + rng.uniform(-4, 6)))

harga_pasar_estimasi = harga_dasar_map[kelas_harga] * rng.uniform(0.92, 1.15)

# ============================================================================
# TAHAP 3 — OUTPUT KE PENGGUNA
# ============================================================================
st.markdown(
    f"<div style='color:{MUTED}; font-size:0.85rem; margin-bottom:0.3rem;'>"
    f"📍 Hasil analisis untuk <b style='color:{NAVY};'>{alamat}</b> · "
    f"Dianalisis {datetime.now().strftime('%d %B %Y, %H:%M')} WIB</div>",
    unsafe_allow_html=True,
)

# --- Skor utama ---
col1, col2 = st.columns(2)

with col1:
    badge_text, badge_bg, badge_fg = score_badge(neighborhood_score)
    st.markdown(
        f"""
        <div class="lm-score-card">
            <div class="lm-algo-tag">🌳 Ditenagai Random Forest</div>
            <div class="lm-score-label">Neighborhood Score</div>
            <div class="lm-score-value" style="color:{score_color(neighborhood_score)};">
                {neighborhood_score}<span class="lm-score-max">/100</span>
            </div>
            <span class="lm-badge" style="background:{badge_bg}; color:{badge_fg};">{badge_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    badge_text2, badge_bg2, badge_fg2 = score_badge(lifestyle_match)
    st.markdown(
        f"""
        <div class="lm-score-card">
            <div class="lm-algo-tag">🎯 Ditenagai K-Nearest Neighbor (KNN)</div>
            <div class="lm-score-label">Lifestyle Match Score — {persona}</div>
            <div class="lm-score-value" style="color:{score_color(lifestyle_match)};">
                {lifestyle_match}<span class="lm-score-max">%</span>
            </div>
            <span class="lm-badge" style="background:{badge_bg2}; color:{badge_fg2};">{badge_text2}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Rincian indikator lingkungan ---
st.markdown(
    """<div class="lm-section-title"><span class="lm-step">02</span> Rincian Indikator Lingkungan</div>""",
    unsafe_allow_html=True,
)

col_chart, col_list = st.columns([1.3, 1])

with col_chart:
    df_ind = pd.DataFrame(
        {"Indikator": list(indikator.keys()), "Skor": list(indikator.values())}
    )
    bar = (
        alt.Chart(df_ind)
        .mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, size=22)
        .encode(
            y=alt.Y("Indikator:N", sort="-x", title=None),
            x=alt.X("Skor:Q", title="Skor (0–100)", scale=alt.Scale(domain=[0, 100])),
            color=alt.condition(
                alt.datum.Skor >= 70,
                alt.value(GREEN),
                alt.condition(alt.datum.Skor >= 50, alt.value(AMBER), alt.value(RED)),
            ),
            tooltip=["Indikator", "Skor"],
        )
        .properties(height=280)
    )
    st.altair_chart(bar, use_container_width=True)

with col_list:
    rows = "".join(
        f"""<div class="lm-indicator">
                <span class="lm-indicator-name">{k}</span>
                <span class="lm-indicator-val" style="color:{score_color(v)};">{v}</span>
            </div>"""
        for k, v in indikator.items()
    )
    st.markdown(f'<div class="lm-card">{rows}</div>', unsafe_allow_html=True)

# --- Community Insight ---
st.markdown(
    """<div class="lm-section-title"><span class="lm-step">03</span> AI Community Insight</div>""",
    unsafe_allow_html=True,
)
st.markdown(
    '<span class="lm-algo-tag">🗣️ Ditenagai NLP, Naive Bayes & LLM API</span>',
    unsafe_allow_html=True,
)

if neighborhood_score >= 80:
    insight = (
        f"Mayoritas ulasan dan diskusi warga di sekitar <b>{alamat}</b> menunjukkan sentimen "
        "positif. Kawasan ini dinilai aman dan tertata, fasilitas mudah dijangkau. Ada beberapa "
        "keluhan kecil soal kepadatan di jam sibuk."
    )
elif neighborhood_score >= 60:
    insight = (
        f"Persepsi warga terhadap <b>{alamat}</b> cenderung netral. Ada laporan "
        "sesekali soal genangan air saat hujan deras, tapi akses fasilitas "
        "umum dinilai cukup memadai."
    )
else:
    insight = (
        f"Beberapa ulasan warga di sekitar <b>{alamat}</b> menyoroti kemacetan dan "
        "minimnya fasilitas umum. Sebaiknya lakukan survei langsung sebelum "
        "memutuskan."
    )
st.markdown(f'<div class="lm-card">💬 {insight}</div>', unsafe_allow_html=True)

# --- Property Value Predictor ---
st.markdown(
    """<div class="lm-section-title"><span class="lm-step">04</span> AI Property Value Predictor</div>""",
    unsafe_allow_html=True,
)
st.markdown(
    '<span class="lm-algo-tag">🧩 Ditenagai simulasi Linear Regression</span>',
    unsafe_allow_html=True,
)

growth = rng.uniform(3, 9)
tahun = list(range(2026, 2031))
proyeksi = [round(harga_pasar_estimasi * (1 + growth / 100) ** i) for i in range(5)]
df_val = pd.DataFrame({"Tahun": tahun, "Estimasi harga (Rp)": proyeksi})
df_val["Tahun"] = df_val["Tahun"].astype(str)

line_chart = (
    alt.Chart(df_val)
    .mark_line(point=alt.OverlayMarkDef(size=70, filled=True, color=GOLD), color=GOLD, strokeWidth=3)
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
    f"Sumbu kiri (Y) selalu menunjukkan **estimasi harga rumah dalam Rupiah**. "
    f"Titik tahun 2026 (Rp{harga_pasar_estimasi:,.0f}".replace(",", ".")
    + f") adalah **estimasi harga pasar saat ini** yang diperkirakan AI dari data historis "
    f"kawasan & kelas harga yang kamu pilih — bukan input manual. Proyeksi memakai asumsi "
    f"pertumbuhan sekitar **{growth:.1f}% per tahun** berdasarkan tren infrastruktur & fasilitas sekitar."
)

st.success("✅ Analisis selesai — hasil di atas adalah simulasi untuk keperluan demo MVP.")

st.markdown("---")
st.markdown(
    "<div class='lm-footer'>LivingMatch AI — Prototipe MVP · Proyek Kewirausahaan · "
    "Jurusan Informatika, Universitas Islam Indonesia</div>",
    unsafe_allow_html=True,
)
