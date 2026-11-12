"""Presentation helpers for the assessment workspace."""
from html import escape
from pathlib import Path

import streamlit as st


def apply_style():
    st.html(f"<style>{Path(__file__).with_name('style.css').read_text()}</style>")


def hero():
    st.html('''<section class="hero">
      <div class="hero-copy"><div class="eyebrow">✦ RUANG KARYA PENDIDIK</div>
      <p class="arabic" lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</p>
      <h1>Asesmen bermakna.<br><span>Ilmu yang bermanfaat.</span></h1>
      <p class="hero-description">Dari materi pelajaran menjadi perangkat asesmen yang terarah.<br> Susun, telaah, dan siapkan dokumen dalam satu ruang kerja.</p>
      <div class="hero-tags"><span>CP · TP · ATP</span><span>Soal &amp; rubrik</span><span>7 dokumen Word</span></div></div>
      <div class="hero-art" aria-hidden="true"><div class="rosette"></div><span>✦</span><p>BERILMU · BERADAB · BERMAKNA</p></div>
    </section>''')


def overview(total, duration, language):
    st.html(f'''<div class="overview">
      <div><span>TARGET ASESMEN</span><strong>{total}<small> butir soal</small></strong></div>
      <div><span>ALOKASI WAKTU</span><strong>{duration}<small> menit</small></strong></div>
      <div><span>BAHASA</span><strong class="language">{escape(language or 'Belum diisi')}</strong></div>
      <div><span>HASIL AKHIR</span><strong>7<small> dokumen Word</small></strong></div>
    </div>''')


def section(number, title, description):
    st.html(f'''<div class="section-heading"><span class="section-number">{number:02d}</span>
      <div><h2>{escape(title)}</h2><p>{escape(description)}</p></div></div>''')


def next_step():
    st.html('''<div class="next-step"><span>TAHAP BERIKUTNYA</span><h3>Soal &amp; dokumen siap pakai</h3>
    <p>Lengkapi materi dan susun tujuan pembelajaran terlebih dahulu. Setelah ditelaah, lanjutkan membuat soal, kunci jawaban, pembahasan, dan rubrik.</p></div>''')
