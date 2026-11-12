# Universal Assessment Generator Pro

Aplikasi Python dan Streamlit untuk menyusun CP, TP, ATP, soal dan tujuh dokumen Word melalui Ollama Cloud. Preset awal memakai Sosiologi XII, semester ganjil, dengan 45 soal. Isian dan jumlah soal dapat diubah.

## Menjalankan

Gunakan Python 3.11 atau 3.12. Ekstrak ZIP, buka terminal di folder yang berisi app.py, lalu jalankan:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Di macOS atau Linux, gunakan `python3` jika perintah `python` tidak tersedia. Buka alamat lokal yang muncul di terminal (biasanya http://localhost:8501).

## Streamlit Secrets

Buat API key di https://ollama.com/settings/keys. Di Streamlit Community Cloud, buka **Advanced settings → Secrets** saat deploy atau **App settings → Secrets** untuk aplikasi yang sudah berjalan. Masukkan:

```toml
OLLAMA_API_KEY = "ganti_dengan_api_key_ollama"
```

Untuk menjalankan secara lokal, buat `.streamlit/secrets.toml` dari `.streamlit/secrets.toml.example`, isi key, lalu mulai ulang Streamlit. Simpan key di pengaturan Secrets atau berkas lokal tersebut. Jangan unggah berkas `secrets.toml` ke GitHub.

## Menggunakan

1. Pastikan API key sudah diatur di Streamlit Secrets. Model bawaan `gpt-oss:120b` dapat diubah dari sidebar. Jika respons AI tidak berbentuk JSON yang valid, ulangi langkah yang gagal.
2. Isi identitas asesmen. Unggah PDF berteks, DOCX, atau TXT berformat UTF-8, atau tempel materi manual. Kedua sumber dapat digabung. Batas unggahan 20 MB dan batas teks gabungan 45.000 karakter. PDF hasil pindai membutuhkan OCR sebelum diunggah.
3. Klik **Isi otomatis CP, TP, dan ATP**. Periksa dan sunting hasil sebelum membuat soal.
4. Klik tombol **Buat soal** sesuai nomor yang tampil hingga jumlahnya lengkap. Batch yang gagal dapat diulang. Progres tersimpan selama sesi Streamlit aktif. Mengubah materi, konfigurasi ujian, atau tujuan pembelajaran dapat memulai ulang generasi soal.
5. Klik **Siapkan tujuh dokumen Word** dan unduh setiap berkas. Guru perlu memeriksa seluruh draf sebelum penggunaan.

Materi dikirim ke Ollama Cloud saat generasi. Hindari data pribadi siswa. Nilai akhir memakai skala 100 berdasarkan total skor mentah pada rubrik.

## Tampilan ruang kerja

Antarmuka memakai palet hijau zamrud, emas, dan gading, dengan basmalah serta ornamen geometris Islami. Sidebar menjelaskan tiga tahap penyusunan; ringkasan menampilkan jumlah soal, durasi, bahasa, dan keluaran dokumen. Tata letak menyesuaikan layar ponsel.

Gaya visual berada di `style.css`, komponen presentasi di `ui.py`, dan tema dasar di `.streamlit/config.toml`. Tidak memerlukan font, gambar, atau dependensi baru dari layanan eksternal. Alur generasi dan ekspor dokumen tetap menggunakan `engine.py`.

## Unduh paket lengkap

Setelah seluruh soal selesai, klik **Siapkan tujuh dokumen Word**, lalu **Unduh semua (ZIP)**. Arsip bernama `Asesmen_Sosiologi_Kelas_XII.zip` (mengikuti input) berisi folder dengan nama yang sama dan tujuh DOCX bernomor. Ekstrak ZIP untuk mendapatkan folder. Unduhan dokumen satu per satu tetap tersedia.
