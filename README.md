# MMin Graduation Photo Upload Tool

Tool internal berbasis Streamlit untuk mengumpulkan foto graduation mahasiswa secara
terpusat. Foto yang diunggah langsung tersimpan ke folder Google Drive admin, dan
setiap upload yang berhasil otomatis dicatat ke Google Spreadsheet (nama, email, link
foto, waktu upload) untuk kebutuhan Graduation Slides.

Koneksi ke Google Drive & Sheets dibuat lewat **Google Apps Script** (bukan Google
Cloud Console) — sepenuhnya gratis dan **tidak memerlukan kartu kredit** sama sekali.

Seluruh data (whitelist email, status upload, link foto) tersimpan **langsung di
Google Spreadsheet** — aplikasi ini sendiri tidak menyimpan database apa pun secara
lokal, sehingga aman untuk dijalankan di layanan hosting mana pun (termasuk yang
tidak menjamin penyimpanan file lokal permanen, seperti Streamlit Community Cloud).

## Fitur

- **Halaman Mahasiswa** (`app.py`)
  1. Mahasiswa memasukkan **email** yang sama seperti saat pendaftaran wisuda.
  2. Email dicek terhadap **whitelist** yang disiapkan admin — jika tidak cocok,
     mahasiswa tidak bisa melanjutkan (tidak ada field lain yang muncul).
  3. Jika email terverifikasi, mahasiswa mengisi **Nama Lengkap** (sesuai yang akan
     dicetak di sertifikat) dan mengunggah **foto** (JPG/PNG, maks 8 MB) dengan preview
     sebelum submit.
  4. Setelah submit: foto diunggah ke folder Google Drive yang ditentukan, dan sebuah
     baris otomatis ditambahkan/diperbarui di tab laporan pada Google Spreadsheet.
  5. Mengunggah ulang dengan email yang sama akan **menggantikan** foto sebelumnya
     (file lama dihapus, foto baru dibuat).
  6. Tersedia toggle **bahasa** (Indonesia/English/中文) dan **tampilan** (terang/gelap).
- **Admin Dashboard** (`pages/1_Admin_Dashboard.py`, dilindungi password)
  - Ringkasan jumlah wisudawan sudah/belum upload.
  - Kelola whitelist email: import CSV (`email,nama`), tempel manual (satu email per
    baris), atau hapus satu email — tersimpan di tab **Whitelist** pada spreadsheet.
  - Tabel status + pencarian/filter, dengan link langsung ke setiap foto di Drive.
  - Galeri foto (thumbnail dari Drive) dengan tombol buka-di-Drive dan hapus.
  - Export CSV status upload. Arsip foto & laporan lengkap selalu tersedia di Google
    Drive + Google Spreadsheet.

## Menjalankan Secara Lokal

Pastikan Python 3.10+ sudah terpasang, lalu dari folder ini:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Setup Google Drive & Sheets via Apps Script (gratis, tanpa kartu kredit)

Ini **bukan** Google Cloud Console — tidak ada verifikasi kartu, tidak ada tagihan.
Anda hanya perlu akun Google biasa (Gmail atau akun kampus).

### 1. Siapkan Folder Drive & Spreadsheet

1. Buat (atau pilih) folder di Google Drive Anda untuk menyimpan foto wisudawan.
   Buka folder tersebut, salin **ID folder** dari URL:
   `https://drive.google.com/drive/folders/`**`ID_FOLDER_INI`**
2. Buat (atau pilih) Google Spreadsheet kosong untuk laporan. Salin **ID
   spreadsheet** dari URL:
   `https://docs.google.com/spreadsheets/d/`**`ID_SPREADSHEET_INI`**`/edit`

### 2. Buat Apps Script

1. Buka [script.google.com](https://script.google.com/) dan login dengan akun Google
   yang sama seperti pemilik folder Drive & spreadsheet di atas.
2. Klik **New project**.
3. Hapus kode default di editor, lalu salin-tempel seluruh isi file
   [`google_apps_script/Code.gs`](google_apps_script/Code.gs) dari project ini.
4. Di bagian atas kode, isi tiga konstanta:
   - `FOLDER_ID` → ID folder Drive dari langkah 1.
   - `SPREADSHEET_ID` → ID spreadsheet dari langkah 1.
   - `SHARED_SECRET` → salin nilai `apps_script_secret` dari
     `.streamlit/secrets.toml` (sudah digenerate otomatis di project ini) supaya
     kedua sisi cocok persis.
5. Beri nama project (misal "MMin Graduation Backend") lalu simpan (Ctrl+S).

### 3. Deploy sebagai Web App

1. Klik tombol **Deploy → New deployment**.
2. Klik ikon gerigi di samping "Select type" → pilih **Web app**.
3. Isi:
   - **Execute as**: `Me` (akun Anda).
   - **Who has access**: `Anyone`.
4. Klik **Deploy**.
5. Akan muncul jendela izin akses — klik **Authorize access**, pilih akun Google
   Anda. Jika muncul peringatan "Google hasn't verified this app", klik
   **Advanced/Lanjutan → Buka [nama project] (unsafe)** — ini aman karena Anda
   sendiri pembuat script-nya.
6. Setelah deploy selesai, salin **Web app URL** yang muncul (formatnya
   `https://script.google.com/macros/s/xxxxx/exec`).

### 4. Hubungkan ke Aplikasi

Isi `.streamlit/secrets.toml`:

```toml
apps_script_url = "https://script.google.com/macros/s/xxxxx/exec"
spreadsheet_url = "https://docs.google.com/spreadsheets/d/ID_SPREADSHEET_INI/edit"
```

(`apps_script_secret` sudah terisi otomatis dan harus sama dengan `SHARED_SECRET`
di Code.gs pada langkah 2.)

### 5. Jalankan Aplikasi

```bash
streamlit run app.py
```

Coba upload satu foto test dari halaman mahasiswa — jika berhasil, foto akan muncul
di folder Drive dan barisnya muncul di spreadsheet dalam beberapa detik.

**Catatan:** setiap kali Anda mengubah isi `Code.gs` di script.google.com, Anda perlu
membuat deployment baru (**Deploy → Manage deployments → Edit → Version: New
version → Deploy**) agar perubahan aktif — URL Web App-nya tetap sama.

## Konfigurasi Password Admin

Password admin diatur di `.streamlit/secrets.toml`:

```toml
admin_password = "ganti-dengan-password-anda"
```

## Struktur Data

- **Tab "Whitelist"** pada spreadsheet Anda — daftar email yang boleh mengunggah foto
  (kolom: Email, Nama).
- **Sheet pertama/utama** pada spreadsheet yang sama — laporan upload (kolom: Nama
  Lengkap, Email, Link Foto, Waktu Upload, Drive File ID, Thumbnail Link).
- Foto asli tersimpan di **folder Google Drive** yang Anda tentukan.
- Aplikasi Streamlit sendiri **tidak menyimpan data apa pun secara lokal** — semua
  state hidup di Google Sheets/Drive, sehingga aman di-restart atau di-deploy ulang
  kapan saja tanpa kehilangan data.
- `.streamlit/secrets.toml` sengaja diabaikan oleh git (lihat `.gitignore`) karena
  berisi kredensial.

## Deploy ke Streamlit Community Cloud (gratis, tanpa kartu kredit)

1. Push kode project ini (kecuali `.streamlit/secrets.toml` — jangan pernah
   di-commit) ke sebuah repository GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io), login dengan akun GitHub.
3. Klik **New app**, pilih repo ini dan file utama `app.py`.
4. Di bagian **Advanced settings → Secrets**, tempel isi `.streamlit/secrets.toml`
   Anda (admin_password, apps_script_url, apps_script_secret, spreadsheet_url).
5. Klik **Deploy** — Anda akan mendapat URL publik seperti
   `https://nama-app.streamlit.app` yang bisa dibagikan ke mahasiswa.

Karena semua data disimpan di Google Sheets/Drive (bukan file lokal), aplikasi ini
aman dijalankan di Streamlit Community Cloud — tidak ada risiko kehilangan whitelist
atau status upload walau container-nya di-restart.

## Format CSV Import Whitelist

```csv
email,nama
budi@kampus.ac.id,Budi Santoso
siti@kampus.ac.id,Siti Aminah
```

Kolom `nama` opsional — hanya untuk referensi admin, bukan yang dicetak di
sertifikat (nama sertifikat diisi sendiri oleh mahasiswa saat upload).

## Catatan Keamanan Akses Foto

Setiap foto yang berhasil diunggah otomatis diberi izin **"Siapa saja yang punya
link dapat melihat"** (`DriveApp.Access.ANYONE_WITH_LINK`) agar tim graduation bisa
langsung membuka link dari spreadsheet tanpa perlu diberi akses folder secara
manual. Jika Anda ingin foto hanya bisa dibuka oleh orang yang sudah diberi akses
ke folder Drive tersebut, hapus baris `file.setSharing(...)` di
`google_apps_script/Code.gs` lalu buat deployment baru.

`SHARED_SECRET` mencegah orang lain memakai Web App Anda walau URL-nya bocor —
jangan bagikan nilai `apps_script_secret` ke luar tim admin.
