"""Editable school-level presets; schools can always enter their own options."""
LANGUAGES = ("Indonesia", "Inggris", "Arab", "Sunda", "Jawa")
LEVELS = ("SD", "SMP", "SMA")
GRADES = {
    "SD": ("I", "II", "III", "IV", "V", "VI"),
    "SMP": ("VII", "VIII", "IX"),
    "SMA": ("X", "XI", "XII"),
}
DEFAULT_GRADES = {"SD": "I", "SMP": "VII", "SMA": "XII"}
RELIGION = (
    "Pendidikan Agama Islam dan Budi Pekerti",
    "Pendidikan Agama Kristen dan Budi Pekerti",
    "Pendidikan Agama Katolik dan Budi Pekerti",
    "Pendidikan Agama Hindu dan Budi Pekerti",
    "Pendidikan Agama Buddha dan Budi Pekerti",
    "Pendidikan Agama Khonghucu dan Budi Pekerti",
)
LOCAL = ("Bahasa Sunda", "Bahasa Jawa", "Bahasa Daerah", "Muatan Lokal")
MADRASAH = ("Bahasa Arab", "Al-Qur'an Hadis", "Akidah Akhlak", "Fikih", "Sejarah Kebudayaan Islam")
ARTS = ("Seni Budaya", "Seni Musik", "Seni Rupa", "Seni Tari", "Seni Teater")


def subject_options(level, grade):
    common = (*RELIGION, "Pendidikan Pancasila", "Bahasa Indonesia", "Matematika", "Bahasa Inggris", "PJOK", *ARTS)
    if level == "SD":
        extra = () if grade in ("I", "II") else ("IPAS", "IPA", "IPS")
    elif level == "SMP":
        extra = ("IPA", "IPS", "Informatika", "Prakarya")
    elif level == "SMA":
        extra = ("IPA", "IPS", "Fisika", "Kimia", "Biologi", "Sejarah", "Geografi", "Ekonomi", "Sosiologi",
                 "Informatika", "Prakarya dan Kewirausahaan", "Matematika Tingkat Lanjut",
                 "Bahasa Indonesia Tingkat Lanjut", "Bahasa Inggris Tingkat Lanjut", "Antropologi",
                 "Bahasa Jepang", "Bahasa Jerman", "Bahasa Prancis", "Bahasa Mandarin", "Bahasa Korea")
    else:
        # An unfamiliar/manual school level gets the combined presets, not an SMA-only list.
        return tuple(dict.fromkeys(subject for name in LEVELS for subject in subject_options(name, "VI" if name == "SD" else GRADES[name][-1])))
    return tuple(dict.fromkeys((*common, *extra, *MADRASAH, *LOCAL)))
