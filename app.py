import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="LivingMatch AI", page_icon="🏡", layout="centered")

# ------------------------------------------------------------------
# THEME / STYLING
# ------------------------------------------------------------------
PRIMARY = "#0F6E4F"      # hijau tua (syariah / trust)
PRIMARY_LIGHT = "#E8F5EE"
GOLD = "#B8860B"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #FAFAF7;
    }}
    .lm-hero {{
        background: linear-gradient(135deg, {PRIMARY} 0%, #0B4A36 100%);
        padding: 28px 28px;
        border-radius: 16px;
        color: white;
        margin-bottom: 18px;
    }}
    .lm-hero h1 {{
        margin: 0;
        font-size: 28px;
        font-weight: 700;
    }}
    .lm-hero p {{
        margin: 6px 0 0 0;
        opacity: 0.9;
        font-size: 15px;
    }}
    .lm-badge {{
        display: inline-block;
        background: {GOLD};
        color: white;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 10px;
        letter-spacing: 0.3px;
    }}
    .lm-card {{
        background: white;
        border: 1px solid #E5E5E0;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 14px;
    }}
    .lm-section-title {{
        font-size: 18px;
        font-weight: 700;
        color: #1A1A1A;
        margin-bottom: 2px;
    }}
    .lm-section-sub {{
        font-size: 13px;
        color: #6B6B6B;
        margin-bottom: 6px;
    }}
    .lm-algo-tag {{
        display: inline-block;
        background: {PRIMARY_LIGHT};
        color: {PRIMARY};
        border: 1px solid #CFE9DC;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 11.5px;
        font-weight: 600;
        margin-bottom: 12px;
    }}
    div[data-testid="stMetric"] {{
        background: {PRIMARY_LIGHT};
        border-radius: 12px;
        padding: 14px 16px;
        border: 1px solid #D3EBDF;
    }}
    div[data-testid="stMetricValue"] {{
        color: {PRIMARY};
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
        background-color: #0B4A36;
        color: white;
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
        <div class="lm-badge">PROTOTIPE MVP · KEWIRAUSAHAAN SYARIAH</div>
        <h1>🏡 LivingMatch AI</h1>
        <p>Asisten AI untuk menganalisis kualitas lingkungan sebelum membeli rumah —
        mengurangi ketimpangan informasi (information asymmetry) antara pembeli, agen,
        dan penjual, selaras dengan prinsip transparansi transaksi ala syariah.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "**Catatan prototipe (MVP):** skor & estimasi harga di bawah dihasilkan dari "
    "simulasi berbasis aturan (rule-based), bukan model Machine Learning yang sudah "
    "dilatih dengan data riil. Tampilan ini merepresentasikan alur dan bentuk output "
    "yang akan dihasilkan sistem Random Forest, KNN, NLP+Naive Bayes+LLM, dan Linear "
    "Regression pada versi produksi."
)

# ------------------------------------------------------------------
# FORM
# ------------------------------------------------------------------
st.markdown('<div class="lm-section-title">1. Lokasi & preferensi</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="lm-section-sub">Masukkan rumah yang sedang kamu incar — AI yang akan '
    'memperkirakan kondisi lingkungan dan estimasi harganya, kamu tidak perlu tahu angkanya duluan.</div>',
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
            "Dekat fasilitas umum",
            "Potensi kenaikan nilai investasi",
        ],
        default=["Keamanan", "Bebas banjir"],
    )

    submitted = st.form_submit_button("🔍 Analisis lingkungan")

if submitted and not alamat:
    st.warning("Isi dulu alamat atau kawasan yang mau dianalisis.")

if submitted and alamat:
    # Seed pakai alamat supaya hasil konsisten tiap kali alamat yang sama dianalisis
    rng = random.Random(alamat)

    # --- Simulasi Neighborhood Score (merepresentasikan output Random Forest) ---
    indikator = {
        "Keamanan": rng.randint(55, 95),
        "Bebas banjir": rng.randint(40, 95),
        "Kualitas udara": rng.randint(50, 90),
        "Kelancaran lalu lintas": rng.randint(35, 90),
        "Fasilitas umum": rng.randint(60, 95),
    }
    neighborhood_score = round(sum(indikator.values()) / len(indikator))

    # --- Simulasi Lifestyle Match Score (merepresentasikan output KNN) ---
    bobot_prioritas = len(prioritas) if prioritas else 1
    lifestyle_score = min(
        98, round(neighborhood_score * 0.8 + bobot_prioritas * 3 + rng.randint(-5, 5))
    )

    # --- Simulasi estimasi harga pasar saat ini ---
    # Merepresentasikan "data historis transaksi" yang dalam produksi diambil dari
    # basis data pasar properti, bukan diinput manual oleh user.
    rentang_harga = {
        "Menengah": (300_000_000, 800_000_000),
        "Menengah-atas": (800_000_000, 2_000_000_000),
        "Premium": (2_000_000_000, 8_000_000_000),
    }
    low, high = rentang_harga[budget]
    harga_pasar_estimasi = round(rng.randint(low, high) / 5_000_000) * 5_000_000

    st.markdown("---")
    st.markdown('<div class="lm-section-title">2. Hasil analisis</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="lm-section-sub">Ringkasan untuk <b>{alamat}</b></div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Neighborhood Score", f"{neighborhood_score}/100")
    c2.metric("Lifestyle Match Score", f"{lifestyle_score}%")
    c3.metric("Estimasi Harga Pasar", f"Rp{harga_pasar_estimasi:,.0f}".replace(",", "."))

    st.markdown("**Rincian indikator lingkungan**")
    st.markdown(
        '<span class="lm-algo-tag">🧩 Ditenagai simulasi Random Forest</span>',
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
        .properties(height=220)
    )
    st.altair_chart(bar_chart, use_container_width=True)

    # --- Simulasi Community Insight (merepresentasikan output NLP + Naive Bayes + LLM) ---
    st.markdown("**Community Insight**")
    st.markdown(
        '<span class="lm-algo-tag">🧩 Ditenagai simulasi NLP + Naive Bayes + ringkasan LLM</span>',
        unsafe_allow_html=True,
    )
    if neighborhood_score >= 80:
        insight = (
            f"Warga sekitar {alamat} umumnya memberi ulasan positif. Lingkungan "
            "dinilai aman dan tertata, fasilitas mudah dijangkau. Ada beberapa "
            "keluhan kecil soal kepadatan di jam sibuk."
        )
    elif neighborhood_score >= 60:
        insight = (
            f"Persepsi warga terhadap {alamat} cenderung netral. Ada laporan "
            "sesekali soal genangan air saat hujan deras, tapi akses fasilitas "
            "umum dinilai cukup memadai."
        )
    else:
        insight = (
            f"Beberapa ulasan warga di sekitar {alamat} menyoroti kemacetan dan "
            "minimnya fasilitas umum. Sebaiknya lakukan survei langsung sebelum "
            "memutuskan."
        )
    st.markdown(f'<div class="lm-card">💬 {insight}</div>', unsafe_allow_html=True)

    # --- Simulasi Property Value Predictor (merepresentasikan output Linear Regression) ---
    st.markdown("**Prediksi tren nilai properti (5 tahun ke depan)**")
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
        .mark_line(point=True, color=GOLD, strokeWidth=3)
        .encode(
            x=alt.X("Tahun:N", title="Tahun"),
            y=alt.Y(
                "Estimasi harga (Rp):Q",
                title="Estimasi harga rumah (Rp)",
                axis=alt.Axis(format="~s"),
                scale=alt.Scale(zero=False),
            ),
            tooltip=[
                "Tahun",
                alt.Tooltip("Estimasi harga (Rp):Q", format=",.0f"),
            ],
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

    st.success("Analisis selesai — hasil di atas adalah simulasi untuk keperluan demo MVP.")

st.markdown("---")
st.caption("LivingMatch AI — Prototipe MVP · Proyek Kewirausahaan Syariah")
