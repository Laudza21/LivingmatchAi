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
        margin-bottom: 14px;
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
        <p>Analisis kualitas lingkungan berbasis AI untuk keputusan pembelian rumah,
        selaras dengan prinsip transparansi dan kehati-hatian ala keuangan syariah.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "**Catatan prototipe (MVP):** skor di bawah dihitung dengan simulasi berbasis "
    "aturan, bukan model Machine Learning yang sudah dilatih dengan data lingkungan "
    "riil. Ini merepresentasikan alur dan bentuk output yang akan dihasilkan sistem "
    "KNN, Random Forest, dan NLP+LLM pada versi produksi."
)

# ------------------------------------------------------------------
# FORM
# ------------------------------------------------------------------
st.markdown('<div class="lm-section-title">1. Lokasi & preferensi</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="lm-section-sub">Masukkan data rumah yang sedang kamu pertimbangkan.</div>',
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
            "Kelas harga rumah", options=["Menengah", "Menengah-atas", "Premium"]
        )

    harga_saat_ini = st.number_input(
        "Harga rumah saat ini (Rp) — opsional, untuk estimasi nilai ke depan",
        min_value=0,
        value=0,
        step=50_000_000,
        format="%d",
        help="Kosongkan (biarkan 0) jika hanya ingin melihat estimasi dalam persentase kenaikan, bukan nominal Rupiah.",
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

    st.markdown("---")
    st.markdown('<div class="lm-section-title">2. Hasil analisis</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="lm-section-sub">Ringkasan untuk <b>{alamat}</b></div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    c1.metric("Neighborhood Score", f"{neighborhood_score}/100")
    c2.metric("Lifestyle Match Score", f"{lifestyle_score}%")

    st.markdown("**Rincian indikator lingkungan**")
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

    # --- Simulasi Community Insight (merepresentasikan output NLP + LLM) ---
    st.markdown("**Community Insight**")
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

    growth = rng.uniform(3, 9)
    tahun = list(range(2026, 2031))

    if harga_saat_ini > 0:
        # Tampilkan dalam Rupiah asli, bukan indeks abstrak — ini yang bikin jelas
        proyeksi = [round(harga_saat_ini * (1 + growth / 100) ** i) for i in range(5)]
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
            f"Sumbu kiri (Y) menunjukkan **estimasi harga rumah dalam Rupiah**, "
            f"dihitung dari harga awal Rp{harga_saat_ini:,.0f} dengan asumsi "
            f"pertumbuhan sekitar **{growth:.1f}% per tahun**."
        )
    else:
        # Tanpa harga awal → tampilkan sebagai persentase kenaikan relatif, dijelaskan gamblang
        proyeksi = [round((1 + growth / 100) ** i - 1, 3) * 100 for i in range(5)]
        df_val = pd.DataFrame({"Tahun": tahun, "Kenaikan nilai relatif (%)": proyeksi})
        df_val["Tahun"] = df_val["Tahun"].astype(str)

        line_chart = (
            alt.Chart(df_val)
            .mark_line(point=True, color=GOLD, strokeWidth=3)
            .encode(
                x=alt.X("Tahun:N", title="Tahun"),
                y=alt.Y(
                    "Kenaikan nilai relatif (%):Q",
                    title="Kenaikan nilai dibanding tahun 2026 (%)",
                ),
                tooltip=[
                    "Tahun",
                    alt.Tooltip("Kenaikan nilai relatif (%):Q", format=".1f"),
                ],
            )
            .properties(height=260)
        )
        st.altair_chart(line_chart, use_container_width=True)
        st.caption(
            f"Sumbu kiri (Y) menunjukkan **persentase kenaikan nilai dibanding harga tahun 2026** "
            f"(bukan nominal Rupiah, karena harga awal belum diisi). Estimasi pertumbuhan: "
            f"sekitar **{growth:.1f}% per tahun**. Isi kolom 'Harga rumah saat ini' di atas "
            f"untuk melihat estimasi dalam Rupiah."
        )

    st.success("Analisis selesai — hasil di atas adalah simulasi untuk keperluan demo MVP.")

st.markdown("---")
