import base64

import requests

from .config import APPS_SCRIPT_SECRET, APPS_SCRIPT_URL


class AppsScriptError(Exception):
    pass


def _call(payload: dict) -> dict:
    if not APPS_SCRIPT_URL:
        raise AppsScriptError(
            "apps_script_url belum diisi di .streamlit/secrets.toml. "
            "Lihat README.md bagian setup Google Apps Script."
        )
    payload = {**payload, "secret": APPS_SCRIPT_SECRET}
    resp = requests.post(APPS_SCRIPT_URL, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("ok"):
        raise AppsScriptError(data.get("error", "Terjadi kesalahan tidak diketahui."))
    return data


def check_email(email: str) -> dict:
    """Returns {"whitelisted": bool, "existing": dict | None}."""
    data = _call({"action": "check_email", "email": email})
    return {"whitelisted": data["whitelisted"], "existing": data.get("existing")}


def submit_photo(email: str, nama: str, filename: str, mime_type: str, file_bytes: bytes) -> dict:
    """Uploads the photo to Drive and upserts the report row, all in one call.

    Returns {"link": str, "thumbnail": str, "timestamp": str}.
    """
    data = _call(
        {
            "action": "submit_photo",
            "email": email,
            "nama": nama,
            "filename": filename,
            "mime_type": mime_type,
            "file_base64": base64.b64encode(file_bytes).decode("ascii"),
        }
    )
    return {"link": data["link"], "thumbnail": data["thumbnail"], "timestamp": data["timestamp"]}


def list_whitelist() -> list[dict]:
    data = _call({"action": "list_whitelist"})
    return data["items"]


def add_whitelist(items: list[dict]) -> int:
    """`items` is a list of {"email": str, "nama": str}. Returns count processed."""
    data = _call({"action": "add_whitelist", "items": items})
    return data["count"]


def remove_whitelist(email: str):
    _call({"action": "remove_whitelist", "email": email})


def list_report() -> list[dict]:
    data = _call({"action": "list_report"})
    return data["items"]


def delete_report_row(email: str):
    _call({"action": "delete_report_row", "email": email})
