import hashlib
import json
import os

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from engine import (MAX_CHARS, MODEL, TITLES, TYPES, curriculum, export_doc,
                    extract, generate_batch, plan, validate_curriculum, document_filename, document_title)

from ui import apply_style, hero, next_step, overview, section

st.set_page_config(page_title="Universal Assessment Generator Pro", page_icon="✦", layout="wide")
apply_style()
hero()

try:
    secret_key = st.secrets.get("OLLAMA_API_KEY")
except StreamlitSecretNotFoundError:
    secret_key = None
key = secret_key.strip() if isinstance(secret_key, str) else ""

with st.sidebar:
    st.html('<div class="sidebar-brand"><span class="brand-mark">✦</span><div><strong>Universal Assessment</strong><small>GENERATOR PRO</small></div></div>')
    st.html('<div class="side-label">ALUR PENYUSUNAN</div><div class="side-step"><span>01</span>Siapkan materi</div><div class="side-step"><span>02</span>Susun tujuan pembelajaran</div><div class="side-step"><span>03</span>Soal &amp; dokumen</div>')
    st.divider()
    st.subheader("Pengaturan AI")
    model = st.text_input("Model Ollama Cloud", value=os.getenv("OLLAMA_MODEL") or MODEL).strip()
    st.html('<div class="connection ready">● Kunci AI tersedia</div>' if key else '<div class="connection">○ Koneksi AI belum diatur</div>')
    st.caption("Kunci dikonfigurasi oleh admin melalui Streamlit Secrets.")
    st.caption("Materi dikirim ke Ollama Cloud saat tombol generasi ditekan. Hindari memasukkan data pribadi siswa.")
    st.html('<p class="sidebar-note">✦ Dibantu AI, ditelaah pendidik.<br>Setiap draf adalah awal karya. Ketelitian dan pertimbangan guru menyempurnakannya.</p>')

st.caption("RUANG KERJA / PENYUSUNAN ASESMEN")
with st.expander("Identitas & komposisi asesmen", expanded=True):
    c1, c2, c3 = st.columns(3)
    jenjang = c1.text_input("Jenjang", "SMA")
    kelas = c2.text_input("Kelas", "XII")
    semester = c3.text_input("Semester", "Ganjil")
    kurikulum = c1.text_input("Kurikulum", "Kurikulum Merdeka")
    mapel = c2.text_input("Mata pelajaran", "Sosiologi")
    bahasa = c3.text_input("Bahasa soal", "Indonesia")
    topik = st.text_input("Topik atau bab", "Bab 1 Perubahan Sosial dan Bab 2 Globalisasi dan Masyarakat Digital")
    columns = st.columns(5)
    counts = [int(col.number_input(label, 0, 100, value, step=1))
              for col, label, value in zip(columns, TYPES, (30, 10, 3, 2))]
    durasi = int(columns[-1].number_input("Durasi (menit)", 1, 360, 90, step=1))
    st.caption(f"Total {sum(counts)} butir • Opsi PG A–E • PG penalaran C4–C5 • Esai penalaran C4–C6")

config = dict(jenjang=jenjang, kelas=kelas, semester=semester, kurikulum=kurikulum,
              mapel=mapel, bahasa=bahasa, topik=topik, jumlah=counts, durasi=durasi)
overview(sum(counts), durasi, bahasa)
section(1, "Materi pelajaran", "Mulai dari sumber yang tepat. Unggah bahan ajar atau tulis materi Anda.")
uploaded = st.file_uploader("Unggah PDF berteks, DOCX, atau TXT • maksimum 20 MB", type=["pdf", "docx", "txt"])
manual = st.text_area("Tulis atau tempel materi manual", height=180,
                      placeholder="Contoh: perubahan sosial mencakup perubahan pola interaksi, nilai, norma, dan lembaga sosial.")
material_parts = []
file_error = False
if uploaded:
    raw = uploaded.getvalue()
    fingerprint = (uploaded.name, hashlib.sha256(raw).hexdigest())
    if st.session_state.get("file_id") != fingerprint:
        try:
            st.session_state["file_text"] = extract(uploaded.name, raw)
            st.session_state["file_error"] = ""
        except ValueError as exc:
            st.session_state["file_error"] = str(exc)
        except Exception:
            st.session_state["file_error"] = "File tidak dapat dibaca. Coba simpan ulang atau tempel teksnya."
        st.session_state["file_id"] = fingerprint
    if st.session_state["file_error"]:
        st.error(st.session_state["file_error"])
        file_error = True
    else:
        material_parts.append("Materi unggahan:\n" + st.session_state["file_text"])
        with st.expander("Pratinjau teks dari file"):
            st.text(st.session_state["file_text"][:4000])
if manual.strip():
    material_parts.append("Materi manual:\n" + manual.strip())
material = "\n\n".join(material_parts)
st.caption(f"{len(material):,} dari {MAX_CHARS:,} karakter materi. Jika diisi keduanya, materi digabung.")

def signature(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True).encode()).hexdigest()

source_config = {k: v for k, v in config.items() if k not in ("jumlah", "durasi", "bahasa")}
source_id = signature([source_config, material])
valid_source = all(str(value).strip() for value in source_config.values()) and bool(material) and not file_error
if len(material) > MAX_CHARS:
    st.error("Materi melampaui batas karakter. Ringkas isinya atau unggah bagian yang akan diujikan.")
    valid_source = False
if not key:
    st.info("Admin perlu menambahkan OLLAMA_API_KEY di Streamlit Secrets untuk mengaktifkan generasi.")
elif not model:
    st.info("Isi model Ollama Cloud untuk menjalankan generasi.")

section(2, "Tujuan pembelajaran", "Susun CP, TP, dan ATP yang selaras dengan materi, lalu telaah hasilnya.")
if st.button("Isi otomatis CP, TP, dan ATP", type="primary", disabled=not (valid_source and key and model)):
    with st.spinner("Ollama Cloud sedang menyusun tujuan pembelajaran…"):
        try:
            outline = curriculum(key, model, source_config, material)
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.session_state["outline"] = outline
            st.session_state["source_id"] = source_id
            st.session_state["outline_rev"] = st.session_state.get("outline_rev", 0) + 1
if st.session_state.get("source_id") != source_id:
    if st.session_state.get("outline"):
        st.info("Materi atau identitas pembelajaran berubah. Isi ulang CP, TP, dan ATP untuk melanjutkan.")
    next_step()
    st.stop()

st.caption("Draf AI — perlu verifikasi guru. Isi dapat disunting sebelum membuat soal.")
base = st.session_state["outline"]
rev = st.session_state["outline_rev"]
cp = st.text_area("Capaian Pembelajaran", base["cp"], key=f"cp_{rev}", height=125)
st.subheader("Tujuan Pembelajaran")
tp = st.data_editor(base["tp"], key=f"tp_{rev}", hide_index=True, width="stretch")
st.subheader("Alur Tujuan Pembelajaran")
atp = st.data_editor(base["atp"], key=f"atp_{rev}", hide_index=True, width="stretch")
try:
    outline = validate_curriculum({"cp": cp, "tp": tp, "atp": atp})
except ValueError as exc:
    st.warning(str(exc))
    st.stop()

st.download_button(f"Unduh {document_title(0, config)}", export_doc(0, config, outline, []),
                   file_name=document_filename(0, config),
                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

section(3, "Soal & dokumen", "Bangun asesmen bertahap, kemudian siapkan tujuh dokumen Word.")
targets = plan(config)
if not targets or not bahasa.strip():
    st.warning("Isi bahasa soal dan tetapkan sedikitnya satu butir.")
    st.stop()
job_id = signature([source_id, config, outline])
if st.session_state.get("job_id") != job_id:
    st.session_state["job_id"] = job_id
    st.session_state["items"] = []
    st.session_state.pop("exports", None)
items = st.session_state["items"]
current = len(items)
progress = st.progress(current / len(targets), text=f"{current}/{len(targets)} butir siap")
batch = targets[current:current + 5]
if batch:
    st.caption("Setiap klik membuat hingga lima soal. Jika satu batch gagal, hasil batch sebelumnya tetap tersedia selama sesi aktif.")
    if st.button(f"Buat soal {batch[0]['nomor']}–{batch[-1]['nomor']}", disabled=not (key and model)):
        with st.spinner("Ollama Cloud sedang menyusun soal dan pembahasannya…"):
            try:
                result = generate_batch(key, model, config, material, outline, batch, items)
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.session_state["items"] = items + result
                st.rerun()
if items:
    with st.expander("Pratinjau soal"):
        for question in items:
            st.text(f"{question['nomor']}. {question['naskah']}")
            for letter, option in zip("ABCDE", question["opsi"]):
                st.text(f"{letter}. {option}")
if current == len(targets):
    st.success("Jumlah dan nomor butir lengkap. Periksa kunci, pembahasan, dan rubrik sebelum digunakan.")
    if st.button("Siapkan tujuh dokumen Word"):
        st.session_state["exports"] = [export_doc(i, config, outline, items) for i in range(len(TITLES))]
    if "exports" in st.session_state:
        for index, (title, data) in enumerate(zip(TITLES, st.session_state["exports"]), 1):
            filename = document_filename(index - 1, config)
            st.download_button(f"Unduh {index:02d} {document_title(index - 1, config)}", data, file_name=filename,
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                               key=f"download_{index}")
