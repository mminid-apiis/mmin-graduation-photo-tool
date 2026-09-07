import streamlit as st

LANGUAGES = {
    "id": "Indonesia",
    "en": "English",
    "zh": "中文",
}

_TRANSLATIONS = {
    "id": {
        "app_title": "🎓 Upload Foto Graduation",
        "app_subtitle": (
            "Unggah foto Anda untuk keperluan **Graduation Slides**. "
            "Baca dulu panduan di bawah ini sebelum mengisi form."
        ),
        "privacy_notice": (
            "🔒 Data (nama, email, dan foto) yang Anda kirimkan hanya digunakan oleh "
            "panitia untuk keperluan administrasi wisuda (Graduation Slides) dan tidak "
            "dibagikan ke pihak lain."
        ),
        "guide_title": "📋 Panduan Sebelum Upload — WAJIB DIBACA",
        "guide_body": """
**1. Email**
Gunakan email yang **sama persis** seperti saat pendaftaran program MMin
Indonesia. Email ini dipakai untuk verifikasi otomatis — jika berbeda, Anda
tidak akan bisa melanjutkan upload.

**2. Nama Lengkap**
⚠️ **Periksa ejaan dengan teliti.** Mohon isi **tanpa** menyertakan gelar
pendidikan Anda — hanya nama lengkap saja. Nama yang Anda ketik akan dicetak
**apa adanya** di sertifikat dan slide wisuda (termasuk huruf besar/kecil).
Kesalahan penulisan nama menjadi tanggung jawab mahasiswa.

**3. Ketentuan Foto**
- **Pakaian**: formal/professional — jas atau blazer berwarna gelap dipadu
  kemeja/blouse polos berwarna terang (putih dianjurkan). **Tidak menerima**
  kaos, kemeja kasual, atau pakaian bermotif ramai.
- **Latar belakang**: polos, berwarna gelap (navy/biru tua/abu gelap), tidak
  ramai dan tidak bermotif.
- **Pose**: menghadap lurus ke kamera, badan tegak, ekspresi natural.
- **Framing**: foto **dari dada/bahu ke atas**, wajah berada di tengah frame,
  pencahayaan merata (tidak gelap, tidak backlit).
- **Format file**: JPG atau PNG, maksimal 8 MB.
""",
        "example_caption": "Contoh foto yang sesuai ketentuan:",
        "email_label": "Email",
        "email_placeholder": "Email yang Anda gunakan saat pendaftaran wisuda",
        "email_not_whitelisted": (
            "Email ini tidak terdaftar sebagai wisudawan. Pastikan Anda memasukkan email "
            "yang sama seperti saat pendaftaran, atau hubungi panitia wisuda jika ini adalah kesalahan."
        ),
        "email_verified": "Email terverifikasi. Silakan lanjutkan mengisi data di bawah.",
        "already_uploaded_info": (
            "Anda sudah pernah mengunggah foto pada **{date}**. "
            "Mengunggah foto baru di bawah ini akan menggantikan foto sebelumnya."
        ),
        "nama_label": "Nama Lengkap (sesuai yang akan dicetak di sertifikat)",
        "nama_placeholder": "Contoh: Budi Santoso",
        "nama_warning_caption": (
            "⚠️ Periksa kembali ejaan nama Anda — nama ini akan dicetak di sertifikat."
        ),
        "file_uploader_label": "Pilih Foto Graduation",
        "preview_caption": "Preview foto Anda",
        "upload_button": "Unggah Foto",
        "error_nama_required": "Nama lengkap wajib diisi.",
        "error_file_required": "Silakan pilih foto untuk diunggah.",
        "generic_upload_error": (
            "Terjadi kesalahan saat mengunggah foto. Silakan coba lagi, "
            "atau hubungi panitia wisuda jika masalah berlanjut."
        ),
        "connection_error": (
            "Tidak dapat memeriksa data Anda saat ini. Silakan muat ulang halaman "
            "dan coba lagi, atau hubungi panitia wisuda jika masalah berlanjut."
        ),
        "spinner_text": "Mengunggah foto...",
        "success_message": "Foto berhasil diunggah untuk **{nama}**. Terima kasih!",
        "confirmed_caption": "Foto yang telah dikonfirmasi",
        "lang_label": "🌐 Bahasa",
        "theme_label": "Tampilan",
        "theme_light": "☀️ Terang",
        "theme_dark": "🌙 Gelap",
    },
    "en": {
        "app_title": "🎓 Graduation Photo Upload",
        "app_subtitle": (
            "Upload your photo for the **Graduation Slides**. "
            "Please read the instructions below before filling out the form."
        ),
        "privacy_notice": (
            "🔒 The data you submit (name, email, and photo) is only used by the "
            "committee for graduation administration (Graduation Slides) and is not "
            "shared with any other party."
        ),
        "guide_title": "📋 Instructions Before Uploading — MUST READ",
        "guide_body": """
**1. Email**
Use the **exact same email** you registered with for the MMin Indonesia
program. This email is used for automatic verification — if it doesn't
match, you won't be able to continue with the upload.

**2. Full Name**
⚠️ **Double-check the spelling carefully.** Please enter it **without** any
academic titles or degrees — full name only. Whatever you type will be
printed **exactly as-is** on the certificate and graduation slide (including
capitalization). Any spelling mistakes are the student's own responsibility.

**3. Photo Requirements**
- **Attire**: formal/professional — a dark-colored suit or blazer paired with
  a plain, light-colored shirt/blouse (white recommended). Casual t-shirts,
  casual shirts, or busy/patterned clothing are **not accepted**.
- **Background**: plain, dark-colored (navy/dark blue/dark gray), not busy or
  patterned.
- **Pose**: facing the camera directly, upright posture, natural expression.
- **Framing**: photo **from chest/shoulders up**, face centered in the frame,
  even lighting (not dark, not backlit).
- **File format**: JPG or PNG, maximum 8 MB.
""",
        "example_caption": "Examples of photos that meet the requirements:",
        "email_label": "Email",
        "email_placeholder": "The email you used when registering for graduation",
        "email_not_whitelisted": (
            "This email is not registered as a graduate. Make sure you enter the same "
            "email you used during registration, or contact the graduation committee if this is a mistake."
        ),
        "email_verified": "Email verified. Please continue filling in the details below.",
        "already_uploaded_info": (
            "You have already uploaded a photo on **{date}**. "
            "Uploading a new photo below will replace the previous one."
        ),
        "nama_label": "Full Name (as it will be printed on the certificate)",
        "nama_placeholder": "e.g., Budi Santoso",
        "nama_warning_caption": (
            "⚠️ Double-check the spelling of your name — it will be printed on the certificate."
        ),
        "file_uploader_label": "Choose Graduation Photo",
        "preview_caption": "Preview of your photo",
        "upload_button": "Upload Photo",
        "error_nama_required": "Full name is required.",
        "error_file_required": "Please select a photo to upload.",
        "generic_upload_error": (
            "An error occurred while uploading the photo. Please try again, "
            "or contact the graduation committee if the problem persists."
        ),
        "connection_error": (
            "Unable to check your data right now. Please reload the page and "
            "try again, or contact the graduation committee if the problem persists."
        ),
        "spinner_text": "Uploading photo...",
        "success_message": "Photo uploaded successfully for **{nama}**. Thank you!",
        "confirmed_caption": "Confirmed photo",
        "lang_label": "🌐 Language",
        "theme_label": "Appearance",
        "theme_light": "☀️ Light",
        "theme_dark": "🌙 Dark",
    },
    "zh": {
        "app_title": "🎓 毕业照片上传",
        "app_subtitle": "请上传您的照片，用于**毕业典礼幻灯片**。请先阅读下方说明，再填写表单。",
        "privacy_notice": "🔒 您提交的数据（姓名、电子邮箱和照片）仅供工作组用于毕业典礼行政事务（毕业典礼幻灯片），不会分享给其他任何一方。",
        "guide_title": "📋 上传前须知——必读",
        "guide_body": """
**1. 电子邮箱**
请使用与报名 MMin Indonesia 项目时**完全相同**的电子邮箱。该邮箱将用于自动验证——如果不一致，您将无法继续上传照片。

**2. 全名**
⚠️ **请仔细检查拼写。** 请**不要**填写任何学位头衔，只需填写全名。您输入的姓名将**原样**印在证书和毕业典礼幻灯片上（包括大小写）。姓名拼写错误由学生本人负责。

**3. 照片要求**
- **着装**：正式/专业着装——深色西装或西装外套搭配素色浅色衬衫/女式衬衫（建议白色）。**不接受**T恤、休闲衬衫或图案繁杂的服装。
- **背景**：纯色深色背景（藏青色/深蓝色/深灰色），不得杂乱或有图案。
- **姿势**：正面直视镜头，身体挺直，表情自然。
- **取景**：照片需**从胸部/肩部以上**拍摄，脸部居中，光线均匀（不过暗，不逆光）。
- **文件格式**：JPG 或 PNG，最大 8 MB。
""",
        "example_caption": "符合要求的照片示例：",
        "email_label": "电子邮箱",
        "email_placeholder": "您报名毕业时使用的电子邮箱",
        "email_not_whitelisted": (
            "该邮箱未被登记为毕业生。请确认您输入的邮箱与报名时使用的邮箱一致，"
            "如有错误请联系毕业典礼工作组。"
        ),
        "email_verified": "邮箱验证成功。请继续填写以下信息。",
        "already_uploaded_info": (
            "您已于 **{date}** 上传过照片。在下方上传新照片将替换之前的照片。"
        ),
        "nama_label": "全名（将按此打印在证书上）",
        "nama_placeholder": "例如：Budi Santoso",
        "nama_warning_caption": "⚠️ 请再次检查姓名拼写——该姓名将被印在证书上。",
        "file_uploader_label": "选择毕业照片",
        "preview_caption": "您的照片预览",
        "upload_button": "上传照片",
        "error_nama_required": "请填写全名。",
        "error_file_required": "请选择要上传的照片。",
        "generic_upload_error": "上传照片时发生错误。请重试，如果问题持续存在，请联系毕业典礼工作组。",
        "connection_error": "目前无法核对您的数据。请重新加载页面后再试，如果问题持续存在，请联系毕业典礼工作组。",
        "spinner_text": "正在上传照片...",
        "success_message": "已成功为 **{nama}** 上传照片。谢谢！",
        "confirmed_caption": "已确认的照片",
        "lang_label": "🌐 语言",
        "theme_label": "外观",
        "theme_light": "☀️ 浅色",
        "theme_dark": "🌙 深色",
    },
}


def get_lang() -> str:
    return st.session_state.get("lang", "id")


def t(key: str, **kwargs) -> str:
    text = _TRANSLATIONS.get(get_lang(), _TRANSLATIONS["id"]).get(key, key)
    return text.format(**kwargs) if kwargs else text
