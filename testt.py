import mimetypes
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any


# =========================
# 1) منطق البرنامج (قابل للاختبار)
# =========================

@dataclass
class FileReport:
    path: str
    filename: str
    size_bytes: int
    extension: str
    mime_type: str
    sha256: str
    is_text: bool
    preview: str
    checks: Dict[str, Any]


def _sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def _guess_is_text(data: bytes) -> bool:
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def run_checks(data: bytes, extension: str, mime_type: str) -> Dict[str, Any]:
    """
    هذه "اختبارات" داخل البرنامج (ليست pytest).
    عدّلها حسب المطلوب.
    """
    results: Dict[str, Any] = {}

    # 1) الحجم
    results["non_empty"] = (len(data) > 0)
    results["size_under_5mb"] = (len(data) <= 5 * 1024 * 1024)

    # 2) الامتداد
    allowed_ext = {".txt", ".md", ".csv", ".json", ".py"}
    results["extension_allowed"] = (extension in allowed_ext)

    # 3) نوع الملف
    results["mime_is_reasonable"] = (mime_type != "application/octet-stream" or extension != "")

    # 4) فحص نصية/باينري
    is_text = _guess_is_text(data)
    results["looks_like_text"] = is_text

    if is_text:
        text = data.decode("utf-8", errors="replace")
        results["contains_at_least_10_chars"] = (len(text.strip()) >= 10)
        results["contains_no_forbidden_word"] = ("forbidden" not in text.lower())
    else:
        results["contains_at_least_10_chars"] = False
        results["contains_no_forbidden_word"] = True

    return results


def analyze_file(path: str, max_preview_chars: int = 600) -> FileReport:
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    data = p.read_bytes()
    ext = p.suffix.lower()
    mime, _ = mimetypes.guess_type(str(p))
    mime = mime or "application/octet-stream"

    is_text = _guess_is_text(data)
    if is_text:
        preview = data.decode("utf-8", errors="replace")[:max_preview_chars]
    else:
        preview = data[:64].hex(" ")

    checks = run_checks(data=data, extension=ext, mime_type=mime)

    return FileReport(
        path=str(p),
        filename=p.name,
        size_bytes=len(data),
        extension=ext,
        mime_type=mime,
        sha256=_sha256_bytes(data),
        is_text=is_text,
        preview=preview,
        checks=checks,
    )


# =========================
# 2) واجهة Desktop Pink (Tkinter)
# =========================

def launch_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox

    root = tk.Tk()
    root.title("Pink File Tester")
    root.geometry("860x560")
    root.minsize(860, 560)

    # Pink Cute Theme
    BG     = "#fff0f6"   # خلفية وردي فاتح
    CARD   = "#ffe4ef"   # بطاقة وردي ناعم
    TEXT   = "#3a0f2e"   # نص غامق مائل للبنفسجي
    MUTED  = "#8b3a62"   # نص ثانوي
    ACCENT = "#ff5fa2"   # وردي قوي للأزرار
    BORDER = "#ff9cc7"   # حدود ناعمة
    BTN    = "#ff7eb6"   # زر وردي
    BTN_HOVER_BG = ACCENT

    root.configure(bg=BG)

    selected_path = tk.StringVar(value="No file selected")

    # إطار رئيسي
    card = tk.Frame(root, bg=CARD, highlightthickness=2, highlightbackground=BORDER)
    card.pack(fill="both", expand=True, padx=18, pady=18)

    header = tk.Frame(card, bg=CARD)
    header.pack(fill="x", padx=16, pady=(14, 8))

    title = tk.Label(
        header,
        text="Local Upload (Browse) + Test",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 16, "bold"),
    )
    title.pack(side="left")

    subtitle = tk.Label(
        header,
        text="No server. Just load the file into the program and test it.",
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 10),
    )
    subtitle.pack(side="left", padx=12)

    path_row = tk.Frame(card, bg=CARD)
    path_row.pack(fill="x", padx=16, pady=(0, 10))

    path_lbl = tk.Label(
        path_row,
        textvariable=selected_path,
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 10),
        anchor="w",
        justify="left",
    )
    path_lbl.pack(fill="x")

    btn_row = tk.Frame(card, bg=CARD)
    btn_row.pack(anchor="w", padx=16, pady=(0, 12))

    def _set_button_style(btn: tk.Button):
        btn.configure(
            bg=BTN,
            fg="white",
            activebackground=BTN_HOVER_BG,
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=9,
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
        )

    def on_browse():
        file_path = filedialog.askopenfilename(title="Choose a file")
        if file_path:
            selected_path.set(file_path)

    def on_upload_and_test():
        path = selected_path.get()
        if not path or path == "No file selected":
            messagebox.showwarning("Missing file", "Select a file first.")
            return

        try:
            report = analyze_file(path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # عرض النتائج
        info_text.delete("1.0", "end")

        info_text.insert("end", "=== FILE INFO ===\n")
        info_text.insert("end", f"Path: {report.path}\n")
        info_text.insert("end", f"Name: {report.filename}\n")
        info_text.insert("end", f"Size: {report.size_bytes} bytes\n")
        info_text.insert("end", f"Extension: {report.extension}\n")
        info_text.insert("end", f"MIME: {report.mime_type}\n")
        info_text.insert("end", f"SHA-256: {report.sha256}\n")
        info_text.insert("end", f"Text file: {report.is_text}\n\n")

        info_text.insert("end", "=== CHECKS ===\n")
        for k, v in report.checks.items():
            status = "PASS" if v else "FAIL"
            info_text.insert("end", f"{status}  {k}\n")

        info_text.insert("end", "\n=== PREVIEW ===\n")
        info_text.insert("end", report.preview)

    browse_btn = tk.Button(btn_row, text="Browse", command=on_browse)
    _set_button_style(browse_btn)
    browse_btn.pack(side="left", padx=(0, 10))

    upload_btn = tk.Button(btn_row, text="Upload + Test", command=on_upload_and_test)
    _set_button_style(upload_btn)
    upload_btn.pack(side="left")

    # صندوق النتائج
    info_text = tk.Text(
        card,
        bg="#fff7fb",
        fg=TEXT,
        insertbackground=TEXT,
        font=("Consolas", 10),
        wrap="word",
        bd=0,
        highlightthickness=2,
        highlightbackground=BORDER,
    )
    info_text.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    # Placeholder
    info_text.insert("end", "Pick a file using Browse, then click Upload + Test.\n")

    root.mainloop()


# =========================
# 3) Unit Tests (pytest) في نفس الملف
# =========================

def test_analyze_file_text(tmp_path):
    file_path = tmp_path / "a.txt"
    file_path.write_text("Hello world, this is a test file.", encoding="utf-8")

    report = analyze_file(str(file_path))

    assert report.filename == "a.txt"
    assert report.extension == ".txt"
    assert report.size_bytes > 0
    assert report.is_text is True
    assert "Hello world" in report.preview
    assert report.checks["non_empty"] is True
    assert report.checks["extension_allowed"] is True


def test_analyze_file_binary(tmp_path):
    file_path = tmp_path / "b.bin"
    file_path.write_bytes(b"\x00\x01\x02\x03\xff\x00\x10")

    report = analyze_file(str(file_path))

    assert report.filename == "b.bin"
    assert report.extension == ".bin"
    assert report.is_text is False
    assert isinstance(report.preview, str)
    assert report.checks["looks_like_text"] is False


# =========================
# تشغيل الواجهة
# =========================

if __name__ == "__main__":
    launch_gui()
