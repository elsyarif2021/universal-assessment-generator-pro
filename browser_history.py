"""Browser-only persistence for completed assessment packages.

Payloads pass through the current Streamlit session; history itself is stored
only by the browser component, never in server files or a shared database.
"""
import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


def history_record(record_id, config, zip_bytes, filename):
    return {
        "id": record_id,
        "subject": config["mapel"],
        "grade": config["kelas"],
        "semester": config["semester"],
        "topic": config["topik"],
        "count": sum(config["jumlah"]),
        "filename": filename,
        "archive": base64.b64encode(zip_bytes).decode("ascii"),
    }


def render_history(record=None):
    # Escape HTML delimiters so user-entered metadata cannot close the script.
    payload = json.dumps(record, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    template = Path(__file__).with_name("browser_history.html").read_text()
    html = template.replace("/*HISTORY_PAYLOAD*/null", payload)
    if hasattr(st, "iframe"):
        st.iframe(html, height=380)
    else:  # Compatibility with the supported Streamlit 1.50 releases.
        components.html(html, height=380, scrolling=True)
