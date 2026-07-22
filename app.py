import random

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="LivingMatch AI", page_icon="🏡", layout="centered")

st.title("🏡 LivingMatch AI")
st.caption("Analisis kualitas lingkungan berbasis AI untuk keputusan pembelian rumah")

st.info(
    "**Catatan prototipe (MVP):** skor di bawah dihitung dengan simulasi berbasis "
    "aturan, bukan model Machine Learning yang sudah dilatih dengan data lingkungan "
    "riil. Ini merepresentasikan alur dan bentuk output yang akan dihasilkan sistem "
    "KNN, Random Forest, dan NLP+LLM pada versi produksi."
)

st.divider()
st.subheader("1. Lokasi & preferensi")

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

    submitted = st.form_submit_button("Analisis lingkungan")

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

    st.divider()
    st.subheader("2. Hasil analisis")

    c1, c2 = st.columns(2)
    c1.metric("Neighborhood Score", f"{neighborhood_score}/100")
    c2.metric("Lifestyle Match Score", f"{lifestyle_score}%")

    st.markdown("**Rincian indikator lingkungan**")
    df = pd.DataFrame(list(indikator.items()), columns=["Indikator", "Skor"]).set_index(
        "Indikator"
    )
    st.bar_chart(df)

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
    st.write(insight)

    # --- Simulasi Property Value Predictor (merepresentasikan output Linear Regression) ---
    st.markdown("**Prediksi tren nilai properti (5 tahun ke depan)**")
    growth = rng.uniform(3, 9)
    tahun = list(range(2026, 2031))
    proyeksi = [round(100 * (1 + growth / 100) ** i) for i in range(5)]
    chart_df = pd.DataFrame(
        {"Tahun": tahun, "Indeks nilai (basis 2026 = 100)": proyeksi}
    ).set_index("Tahun")
    st.line_chart(chart_df)
    st.caption(f"Estimasi pertumbuhan nilai properti: sekitar {growth:.1f}% per tahun.")

    st.success("Analisis selesai — hasil di atas adalah simulasi untuk keperluan demo MVP.")

st.divider()
st.caption("LivingMatch AI — Prototipe MVP · Tugas mata kuliah")
