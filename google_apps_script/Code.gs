// ============================================================================
// MMin Graduation Photo Upload Tool — Google Apps Script backend
//
// Cara pakai: salin SELURUH isi file ini ke script.google.com (lihat panduan
// lengkap di README.md bagian "Setup Google Drive & Sheets via Apps Script").
//
// Semua data (whitelist email & status upload) disimpan langsung di
// spreadsheet ini — tidak ada database lain di luar Google. Ini membuat data
// aman walau aplikasi Streamlit-nya di-restart/redeploy di mana pun.
// ============================================================================

// ==== KONFIGURASI - WAJIB DIISI SEBELUM DEPLOY ====

// ID folder Google Drive tujuan penyimpanan foto.
// Ambil dari URL folder: https://drive.google.com/drive/folders/<ID_INI>
const FOLDER_ID = "ISI_ID_FOLDER_DRIVE_ANDA";

// ID Google Spreadsheet untuk whitelist & laporan otomatis.
// Ambil dari URL spreadsheet: https://docs.google.com/spreadsheets/d/<ID_INI>/edit
const SPREADSHEET_ID = "ISI_ID_SPREADSHEET_ANDA";

// Harus SAMA PERSIS dengan nilai `apps_script_secret` di .streamlit/secrets.toml.
const SHARED_SECRET = "ISI_TEKS_RAHASIA_YANG_SAMA_DENGAN_SECRETS_TOML";

// ============================================================================

const WHITELIST_SHEET_NAME = "Whitelist";
const WHITELIST_HEADER = ["Email", "Nama"];
// Kolom pada sheet laporan (sheet pertama/utama di spreadsheet ini):
// A=Nama Lengkap, B=Email, C=Link Foto, D=Waktu Upload, E=Drive File ID, F=Thumbnail Link

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    if (body.secret !== SHARED_SECRET) {
      return jsonResponse({ ok: false, error: "Unauthorized" });
    }

    switch (body.action) {
      case "check_email":
        return jsonResponse(checkEmail(body));
      case "submit_photo":
        return jsonResponse(submitPhoto(body));
      case "list_whitelist":
        return jsonResponse(listWhitelist());
      case "add_whitelist":
        return jsonResponse(addWhitelist(body));
      case "remove_whitelist":
        return jsonResponse(removeWhitelist(body));
      case "list_report":
        return jsonResponse(listReport());
      case "delete_report_row":
        return jsonResponse(deleteReportRow(body));
      default:
        return jsonResponse({ ok: false, error: "Unknown action: " + body.action });
    }
  } catch (err) {
    return jsonResponse({ ok: false, error: String(err) });
  }
}

// --- Sheet helpers -----------------------------------------------------

function getReportSheet() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = ss.getSheets()[0];
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(["Nama Lengkap", "Email", "Link Foto", "Waktu Upload", "Drive File ID", "Thumbnail Link"]);
  } else {
    // Upgrade header lama secara aman jika kolom E/F belum ada, tanpa
    // mengubah data yang sudah ada di kolom A-D.
    if (!sheet.getRange(1, 5).getValue()) sheet.getRange(1, 5).setValue("Drive File ID");
    if (!sheet.getRange(1, 6).getValue()) sheet.getRange(1, 6).setValue("Thumbnail Link");
  }
  return sheet;
}

function getWhitelistSheet() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  let sheet = ss.getSheetByName(WHITELIST_SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(WHITELIST_SHEET_NAME);
    sheet.appendRow(WHITELIST_HEADER);
  } else if (sheet.getLastRow() === 0) {
    sheet.appendRow(WHITELIST_HEADER);
  }
  return sheet;
}

function normalizeEmail(email) {
  return String(email || "").trim().toLowerCase();
}

// Mencari baris berisi `email` pada kolom ke `emailCol` (0-based).
// Mengembalikan {rowNumber, row} (rowNumber 1-based, siap dipakai getRange) atau null.
function findRowByEmail(sheet, email, emailCol) {
  const data = sheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (normalizeEmail(data[i][emailCol]) === email) {
      return { rowNumber: i + 1, row: data[i] };
    }
  }
  return null;
}

// --- Actions -------------------------------------------------------------

function checkEmail(body) {
  const email = normalizeEmail(body.email);
  const wl = getWhitelistSheet();
  const whitelisted = !!findRowByEmail(wl, email, 0);

  let existing = null;
  if (whitelisted) {
    const report = getReportSheet();
    const match = findRowByEmail(report, email, 1);
    if (match) {
      existing = {
        nama: match.row[0],
        link: match.row[2],
        uploaded_at: match.row[3],
        file_id: match.row[4],
        thumbnail: match.row[5],
      };
    }
  }
  return { ok: true, whitelisted: whitelisted, existing: existing };
}

function submitPhoto(body) {
  const email = normalizeEmail(body.email);
  const nama = body.nama;
  const report = getReportSheet();
  const existing = findRowByEmail(report, email, 1);

  if (existing && existing.row[4]) {
    trashIfInsideFolder(existing.row[4]);
  }

  const folder = DriveApp.getFolderById(FOLDER_ID);
  const bytes = Utilities.base64Decode(body.file_base64);
  const blob = Utilities.newBlob(bytes, body.mime_type, body.filename);
  const file = folder.createFile(blob);
  file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);

  const link = file.getUrl();
  const thumbnail = "https://drive.google.com/thumbnail?id=" + file.getId() + "&sz=w400";
  const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");
  // Prefix dengan ' agar Google Sheets menyimpannya sebagai teks biasa, bukan
  // otomatis dikonversi jadi tipe tanggal (yang berubah format saat dibaca ulang).
  const rowValues = [nama, email, link, "'" + timestamp, file.getId(), thumbnail];

  if (existing) {
    report.getRange(existing.rowNumber, 1, 1, rowValues.length).setValues([rowValues]);
  } else {
    report.appendRow(rowValues);
  }

  return { ok: true, link: link, thumbnail: thumbnail, timestamp: timestamp };
}

function listWhitelist() {
  const wl = getWhitelistSheet();
  const data = wl.getDataRange().getValues();
  const items = [];
  for (let i = 1; i < data.length; i++) {
    const email = normalizeEmail(data[i][0]);
    if (email) items.push({ email: email, nama: data[i][1] || "" });
  }
  return { ok: true, items: items };
}

function addWhitelist(body) {
  const wl = getWhitelistSheet();
  const items = body.items || [];
  let count = 0;
  items.forEach(function (item) {
    const email = normalizeEmail(item.email);
    if (!email) return;
    const nama = item.nama || "";
    const existing = findRowByEmail(wl, email, 0);
    if (existing) {
      if (nama) wl.getRange(existing.rowNumber, 2).setValue(nama);
    } else {
      wl.appendRow([email, nama]);
    }
    count++;
  });
  return { ok: true, count: count };
}

function removeWhitelist(body) {
  const wl = getWhitelistSheet();
  const email = normalizeEmail(body.email);
  const existing = findRowByEmail(wl, email, 0);
  if (existing) wl.deleteRow(existing.rowNumber);
  return { ok: true };
}

function listReport() {
  const report = getReportSheet();
  const data = report.getDataRange().getValues();
  const items = [];
  for (let i = 1; i < data.length; i++) {
    const email = normalizeEmail(data[i][1]);
    if (!email) continue;
    items.push({
      nama: data[i][0],
      email: email,
      link: data[i][2],
      uploaded_at: data[i][3],
      file_id: data[i][4],
      thumbnail: data[i][5],
    });
  }
  return { ok: true, items: items };
}

function deleteReportRow(body) {
  const report = getReportSheet();
  const email = normalizeEmail(body.email);
  const existing = findRowByEmail(report, email, 1);
  if (existing) {
    if (existing.row[4]) trashIfInsideFolder(existing.row[4]);
    report.deleteRow(existing.rowNumber);
  }
  return { ok: true };
}

// Hanya menghapus file yang benar-benar berada di dalam FOLDER_ID — mencegah
// permintaan yang berisi ID sembarangan menghapus file lain di Drive Anda.
function trashIfInsideFolder(fileId) {
  try {
    const file = DriveApp.getFileById(fileId);
    const parents = file.getParents();
    while (parents.hasNext()) {
      if (parents.next().getId() === FOLDER_ID) {
        file.setTrashed(true);
        return;
      }
    }
    // File ditemukan tapi bukan di dalam folder wisuda — abaikan demi keamanan.
  } catch (err) {
    // File tidak ditemukan / sudah terhapus sebelumnya — abaikan.
  }
}

function jsonResponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
