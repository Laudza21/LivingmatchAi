# LivingMatch AI — Prototipe MVP

Aplikasi analisis kualitas lingkungan berbasis Artificial Intelligence untuk membantu keputusan pembelian rumah.

Prototipe ini dibuat untuk memenuhi tugas mata kuliah Kewirausahaan Syariah untuk mendemonstrasikan alur pengguna dan bentuk output dari tiga fitur AI utama (Lifestyle Match Score, Neighborhood Score, Community Insight) tanpa model Machine Learning terlatih penuh. Skor dan insight dihasilkan lewat simulasi berbasis aturan yang merepresentasikan output yang akan dihasilkan algoritma KNN, Random Forest, dan NLP+LLM pada versi produksi.

## Fitur pada prototipe
- Form input alamat, profil pengguna, dan prioritas gaya hidup
- Neighborhood Score — simulasi skor gabungan dari 5 indikator lingkungan
- Lifestyle Match Score — simulasi tingkat kecocokan berdasarkan prioritas yang dipilih
- Community Insight — ringkasan naratif berdasarkan skor lingkungan
- Prediksi tren nilai properti 5 tahun ke depan

## Menjalankan secara lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy ke Streamlit Community Cloud
1. Push folder ini ke repository GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io), login pakai akun GitHub.
3. Klik **New app**, pilih repo ini, branch `main`, dan file utama `app.py`.
4. Klik **Deploy** — link live akan otomatis muncul (format `https://<nama-app>.streamlit.app`).

## Tim
- Laudza Muhammad Anwar Lahiz (23523005)
- Faiz Galen Ganendra (23523110)
