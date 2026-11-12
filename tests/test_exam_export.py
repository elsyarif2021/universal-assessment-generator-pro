import copy
import unittest
from io import BytesIO
from unittest.mock import patch
from zipfile import ZipFile

from docx import Document

from engine import TITLES, TYPES, export_doc, export_zip, generate_batch, plan, validate_items


class ExamExportTests(unittest.TestCase):
    def fixtures(self, count):
        config = dict(mapel="Sosiologi", kelas="XII", jenjang="SMA", semester="Ganjil",
                      kurikulum="Merdeka", topik="Perubahan sosial", durasi=90,
                      bahasa="Indonesia", jumlah=[1, 1, 1, 1], option_count=count)
        outline = {"cp": "Memahami perubahan sosial", "tp": [
            {"id": "TP1", "materi": "Perubahan sosial", "tujuan": "Menganalisis perubahan"}],
            "atp": [{"id": "TP1", "langkah": "Mengkaji contoh"}]}
        rows = []
        for index, kind in enumerate(TYPES, 1):
            pg = kind.startswith("PG")
            rows.append(dict(nomor=index, jenis=kind, tp="TP1", indikator="Analisis contoh",
                             level="C4" if "penalaran" in kind else "C2",
                             naskah=f"{index}. **Pertanyaan {index}**\nBacalah stimulus berikut.",
                             opsi=[f"{letter}. Pilihan {letter}" for letter in "ABCDE"[:count]] if pg else [],
                             kunci="ABCDE"[count - 1] if pg else "Pokok jawaban",
                             kriteria=[] if pg else ["Kriteria 1", "Kriteria 2", "Kriteria 3", "Kriteria 4"],
                             skor=1.5 if pg else 8, pembahasan="Pembahasan khusus guru",
                             analisis="Sesuai tujuan"))
        return config, outline, rows

    def test_all_option_ranges_and_section_layout(self):
        for count in (3, 4, 5):
            with self.subTest(count=count):
                config, outline, rows = self.fixtures(count)
                validate_items({"soal": copy.deepcopy(rows)}, plan(config), {"TP1"}, count)
                doc = Document(BytesIO(export_doc(2, config, outline, rows)))
                texts = [p.text for p in doc.paragraphs]
                self.assertEqual(len(doc.tables), 0)
                self.assertIn("A. Pilihan Ganda (Reguler + TKA/HOTS)", texts)
                self.assertIn("B. Essay (Reguler + TKA/HOTS)", texts)
                self.assertLess(texts.index("A. Pilihan Ganda (Reguler + TKA/HOTS)"),
                                texts.index("B. Essay (Reguler + TKA/HOTS)"))
                self.assertEqual(texts.count("Soal Reguler"), 2)
                self.assertEqual(texts.count("Soal TKA/HOTS"), 2)
                for letter in "ABCDE"[:count]:
                    self.assertEqual(texts.count(f"{letter}. Pilihan {letter}"), 2)
                for letter in "ABCDE"[count:]:
                    self.assertNotIn(f"{letter}. Pilihan {letter}", texts)
                self.assertFalse(any("**" in t or "Pembahasan khusus guru" in t for t in texts))
                self.assertIn("1. Pertanyaan 1\nBacalah stimulus berikut.", texts)
                key = Document(BytesIO(export_doc(3, config, outline, rows)))
                self.assertIn("ABCDE"[count - 1], key.tables[0].rows[1].cells[2].text)

    def test_reject_wrong_option_count_or_key(self):
        for count in (3, 4, 5):
            config, _, rows = self.fixtures(count)
            wrong_count = copy.deepcopy(rows)
            wrong_count[0]["opsi"].append("Opsi tambahan")
            with self.assertRaises(ValueError):
                validate_items({"soal": wrong_count}, plan(config), {"TP1"}, count)
            wrong_key = copy.deepcopy(rows)
            wrong_key[0]["kunci"] = "ABCDE"[count] if count < 5 else "F"
            with self.assertRaises(ValueError):
                validate_items({"soal": wrong_key}, plan(config), {"TP1"}, count)

    def test_actual_generation_validates_selected_range(self):
        for count in (3, 4, 5):
            config, outline, rows = self.fixtures(count)
            with patch("engine.ollama_json", return_value={"soal": rows}) as mocked:
                result = generate_batch("test", "model", config, "materi", outline, plan(config), [])
                self.assertEqual(len(result[0]["opsi"]), count)
                self.assertEqual(mocked.call_args.args[3]["konfigurasi"]["option_count"], count)

    def test_all_exports_and_zip_remain_readable(self):
        for count in (3, 4, 5):
            config, outline, rows = self.fixtures(count)
            documents = [export_doc(i, config, outline, rows) for i in range(len(TITLES))]
            with ZipFile(BytesIO(export_zip(config, documents))) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(len(archive.namelist()), 7)
                for name in archive.namelist():
                    self.assertTrue(Document(BytesIO(archive.read(name))).paragraphs)


if __name__ == "__main__":
    unittest.main()
