import re

from PIL import Image

from .config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES


def validate_photo(uploaded_file):
    """Returns (is_valid: bool, error_message: str)."""
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower() if "." in uploaded_file.name else ""
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Format file .{ext} tidak didukung. Gunakan JPG atau PNG."

    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        size_mb = uploaded_file.size / 1024 / 1024
        limit_mb = MAX_FILE_SIZE_BYTES // 1024 // 1024
        return False, f"Ukuran file terlalu besar ({size_mb:.1f} MB). Maksimal {limit_mb} MB."

    try:
        img = Image.open(uploaded_file)
        img.verify()
    except Exception:
        return False, "File tidak dapat dibaca sebagai gambar. Pastikan file tidak rusak."
    finally:
        uploaded_file.seek(0)

    return True, ""


def safe_filename(name: str) -> str:
    """Strips characters that are awkward in filenames, keeping the name readable."""
    cleaned = re.sub(r'[\\/:*?"<>|]', "", name).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned or "foto"
