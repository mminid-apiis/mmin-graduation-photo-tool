import streamlit as st

from lib.apps_script_client import check_email, submit_photo
from lib.config import BASE_DIR
from lib.i18n import LANGUAGES, get_lang, t
from lib.theme import apply_theme, is_dark
from lib.utils import safe_filename, validate_photo

st.set_page_config(page_title="Graduation Photo Upload", page_icon="🎓", layout="centered")
apply_theme()

lang_col, theme_col = st.columns([2, 1])
with lang_col:
    lang_codes = list(LANGUAGES.keys())
    st.selectbox(
        t("lang_label"),
        options=lang_codes,
        format_func=lambda code: LANGUAGES[code],
        index=lang_codes.index(get_lang()),
        key="lang",
    )
with theme_col:
    st.radio(
        t("theme_label"),
        options=[False, True],
        format_func=lambda d: t("theme_dark") if d else t("theme_light"),
        index=1 if is_dark() else 0,
        key="dark_mode",
        horizontal=True,
    )

st.title(t("app_title"))
st.write(t("app_subtitle"))
st.caption(t("privacy_notice"))

with st.expander(t("guide_title"), expanded=True):
    st.markdown(t("guide_body"))

    example_dir = BASE_DIR / "assets" / "contoh_foto"
    example_photos = sorted(example_dir.glob("*")) if example_dir.exists() else []
    if example_photos:
        st.caption(t("example_caption"))
        cols = st.columns(len(example_photos))
        for col, photo_path in zip(cols, example_photos):
            col.image(str(photo_path), width="stretch")

email = st.text_input(t("email_label"), placeholder=t("email_placeholder")).strip().lower()

if not email:
    st.stop()

try:
    status = check_email(email)
except Exception as e:
    print(f"[check_email_error] email={email} error={e}")
    st.error(t("connection_error"))
    st.stop()

if not status["whitelisted"]:
    st.error(t("email_not_whitelisted"))
    st.stop()

st.success(t("email_verified"))

existing = status["existing"]
if existing:
    st.info(t("already_uploaded_info", date=existing["uploaded_at"]))

nama = st.text_input(
    t("nama_label"),
    value=existing["nama"] if existing else "",
    placeholder=t("nama_placeholder"),
).strip()
st.caption(t("nama_warning_caption"))

uploaded_file = st.file_uploader(t("file_uploader_label"), type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption=t("preview_caption"), width=250)

st.divider()

if st.button(t("upload_button"), type="primary", width="stretch"):
    errors = []
    if not nama:
        errors.append(t("error_nama_required"))
    if not uploaded_file:
        errors.append(t("error_file_required"))

    if errors:
        for e in errors:
            st.error(e)
    else:
        is_valid, msg = validate_photo(uploaded_file)
        if not is_valid:
            st.error(msg)
        else:
            with st.spinner(t("spinner_text")):
                file_bytes = uploaded_file.getvalue()
                ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
                drive_filename = f"{safe_filename(nama)}.{ext}"

                try:
                    submit_photo(email, nama, drive_filename, uploaded_file.type, file_bytes)
                except Exception as e:
                    # Detail teknis hanya dicatat di log server, tidak ditampilkan ke mahasiswa.
                    print(f"[upload_error] email={email} error={e}")
                    st.error(t("generic_upload_error"))
                    st.stop()

            st.success(t("success_message", nama=nama))
            st.image(uploaded_file, caption=t("confirmed_caption"), width=250)
            st.balloons()
