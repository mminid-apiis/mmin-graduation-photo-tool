import pandas as pd
import streamlit as st

from lib.apps_script_client import (
    add_whitelist,
    delete_report_row,
    list_report,
    list_whitelist,
    remove_whitelist,
)
from lib.config import SPREADSHEET_URL

st.set_page_config(page_title="Admin - Graduation Photos", page_icon="🗂️", layout="wide")

st.title("🗂️ Admin Dashboard — Graduation Photo Upload")


def get_admin_password() -> str:
    try:
        return st.secrets["admin_password"]
    except Exception:
        return "admin123"


if "admin_authed" not in st.session_state:
    st.session_state.admin_authed = False

if not st.session_state.admin_authed:
    st.subheader("Login Admin")
    pwd = st.text_input("Password", type="password")
    if st.button("Masuk"):
        if pwd == get_admin_password():
            st.session_state.admin_authed = True
            st.rerun()
        else:
            st.error("Password salah.")
    st.stop()

top_left, top_right = st.columns([6, 1])
with top_right:
    if st.button("Logout", use_container_width=True):
        st.session_state.admin_authed = False
        st.rerun()


def build_overview():
    """Combines the Whitelist and Report sheets into one status list."""
    whitelist = list_whitelist()
    report = list_report()
    report_by_email = {r["email"]: r for r in report}

    overview = []
    for w in whitelist:
        r = report_by_email.get(w["email"])
        overview.append(
            {
                "email": w["email"],
                "nama_whitelist": w["nama"],
                "nama_submitted": r["nama"] if r else None,
                "drive_file_id": r["file_id"] if r else None,
                "drive_link": r["link"] if r else None,
                "thumbnail_link": r["thumbnail"] if r else None,
                "uploaded_at": r["uploaded_at"] if r else None,
            }
        )
    return overview


try:
    overview = build_overview()
except Exception as e:
    st.error(f"Gagal memuat data dari Google Sheets: {e}")
    st.stop()

total = len(overview)
uploaded = sum(1 for s in overview if s["drive_link"])
belum = total - uploaded

c1, c2, c3 = st.columns(3)
c1.metric("Total Whitelist", total)
c2.metric("Sudah Upload", uploaded)
c3.metric("Belum Upload", belum)

if SPREADSHEET_URL:
    st.caption(f"📄 Whitelist & laporan tersimpan di: {SPREADSHEET_URL}")

st.divider()

with st.expander("📥 Kelola Whitelist Email Wisudawan"):
    st.caption(
        "Hanya email yang ada di whitelist ini yang bisa melanjutkan upload foto. "
        "Menambah whitelist tidak akan menimpa foto yang sudah diunggah. "
        "Data whitelist disimpan di tab 'Whitelist' pada spreadsheet laporan."
    )

    tab_csv, tab_paste, tab_remove = st.tabs(["Import CSV", "Tempel Manual", "Hapus Email"])

    with tab_csv:
        st.caption("Kolom yang dibutuhkan: `email` (kolom `nama` opsional).")
        roster_file = st.file_uploader("Pilih file CSV", type=["csv"], key="roster_csv")
        if roster_file and st.button("Proses Import CSV"):
            try:
                df = pd.read_csv(roster_file)
                df.columns = [c.strip().lower() for c in df.columns]
                if "email" not in df.columns:
                    st.error("CSV harus memiliki kolom `email`.")
                else:
                    items = []
                    for _, row in df.iterrows():
                        email_val = str(row["email"]).strip()
                        if not email_val or email_val.lower() == "nan":
                            continue
                        items.append({"email": email_val, "nama": str(row.get("nama", "")).strip()})
                    count = add_whitelist(items)
                    st.success(f"{count} email berhasil ditambahkan/diperbarui di whitelist.")
                    st.rerun()
            except Exception as e:
                st.error(f"Gagal memproses CSV: {e}")

    with tab_paste:
        st.caption("Satu email per baris. Format opsional: `email,nama`.")
        pasted = st.text_area("Daftar Email", height=150, key="paste_emails")
        if st.button("Tambah ke Whitelist"):
            items = []
            for line in pasted.splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",", 1)
                email_val = parts[0].strip()
                nama_val = parts[1].strip() if len(parts) > 1 else ""
                if email_val:
                    items.append({"email": email_val, "nama": nama_val})
            if items:
                try:
                    count = add_whitelist(items)
                    st.success(f"{count} email berhasil ditambahkan/diperbarui di whitelist.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal menambahkan whitelist: {e}")
            else:
                st.warning("Tidak ada email yang valid untuk ditambahkan.")

    with tab_remove:
        remove_email = st.text_input("Email yang akan dihapus dari whitelist")
        if st.button("Hapus dari Whitelist"):
            if remove_email.strip():
                try:
                    remove_whitelist(remove_email.strip())
                    st.success(f"{remove_email.strip()} dihapus dari whitelist.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal menghapus email: {e}")

st.divider()

filter_col, status_col = st.columns([2, 1])
search = filter_col.text_input("Cari Email / Nama")
status_filter = status_col.selectbox("Filter Status", ["Semua", "Sudah Upload", "Belum Upload"])

filtered = overview
if search:
    s_low = search.lower()
    filtered = [
        s
        for s in filtered
        if s_low in s["email"].lower()
        or s_low in (s["nama_submitted"] or "").lower()
        or s_low in (s["nama_whitelist"] or "").lower()
    ]
if status_filter == "Sudah Upload":
    filtered = [s for s in filtered if s["drive_link"]]
elif status_filter == "Belum Upload":
    filtered = [s for s in filtered if not s["drive_link"]]

tab_table, tab_gallery = st.tabs(["📋 Tabel", "🖼️ Galeri Foto"])

with tab_table:
    if filtered:
        df_view = pd.DataFrame(
            [
                {
                    "Email": s["email"],
                    "Nama": s["nama_submitted"] or s["nama_whitelist"] or "-",
                    "Status": "Sudah Upload" if s["drive_link"] else "Belum Upload",
                    "Waktu Upload": s["uploaded_at"] or "-",
                    "Link Foto": s["drive_link"] or "",
                }
                for s in filtered
            ]
        )
        st.dataframe(
            df_view,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Link Foto": st.column_config.LinkColumn("Link Foto", display_text="Buka")
            },
        )

        csv_bytes = df_view.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Export CSV",
            csv_bytes,
            file_name="status_upload_mahasiswa.csv",
            mime="text/csv",
        )
    else:
        st.info("Tidak ada data yang cocok.")

with tab_gallery:
    uploaded_entries = [s for s in filtered if s["drive_link"]]
    if not uploaded_entries:
        st.info("Belum ada foto yang cocok dengan filter ini.")
    else:
        cols_per_row = 4
        rows = [
            uploaded_entries[i : i + cols_per_row]
            for i in range(0, len(uploaded_entries), cols_per_row)
        ]
        for row in rows:
            cols = st.columns(cols_per_row)
            for col, s in zip(cols, row):
                with col:
                    if s["thumbnail_link"]:
                        st.image(s["thumbnail_link"], use_container_width=True)
                    nama = s["nama_submitted"] or s["nama_whitelist"] or "-"
                    st.caption(f"**{nama}**\n\n{s['email']}")
                    st.link_button("Buka di Drive", s["drive_link"], use_container_width=True)
                    if st.button("Hapus", key=f"del_{s['email']}", use_container_width=True):
                        try:
                            delete_report_row(s["email"])
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal menghapus: {e}")
