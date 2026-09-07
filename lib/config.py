from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE_MB = 8
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def _secret(key: str, default: str = "") -> str:
    try:
        return st.secrets[key]
    except Exception:
        return default


# URL deployment Web App dari Google Apps Script (lihat README.md).
APPS_SCRIPT_URL = _secret("apps_script_url")
# Harus sama persis dengan SHARED_SECRET di Code.gs — mencegah orang lain
# memanggil Web App Anda meskipun URL-nya bocor.
APPS_SCRIPT_SECRET = _secret("apps_script_secret")
# Opsional, hanya dipakai untuk menampilkan link "Buka Laporan" di admin dashboard.
SPREADSHEET_URL = _secret("spreadsheet_url")
