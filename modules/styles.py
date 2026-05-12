# modules/styles.py
"""
Template pesan profesional untuk Userbot
Cara penggunaan: from modules.styles import success, error, info, progress, result_box, inline, bold, italic, mono, border
"""

def border(char="━", length=25):
    """Membuat garis batas dengan karakter dan panjang tertentu."""
    return char * length

def _wrap(text, monospace=False):
    """Bungkus teks dengan markdown monospace jika diperlukan."""
    return f"`{text}`" if monospace else text

def success(text, title="✅ BERHASIL", border_char="━", monospace=False):
    """Template pesan sukses dengan border."""
    return f"{title}\n{border(border_char)}\n{_wrap(text, monospace)}"

def error(text, title="❌ GAGAL", border_char="━", monospace=True):
    """Template pesan error dengan border dan teks monospace (default)."""
    return f"{title}\n{border(border_char)}\n{_wrap(text, monospace)}"

def info(text, title="ℹ️ INFO", border_char="━", monospace=False):
    """Template pesan informasi."""
    return f"{title}\n{border(border_char)}\n{_wrap(text, monospace)}"

def warning(text, title="⚠️ PERINGATAN", border_char="━", monospace=False):
    """Template pesan peringatan."""
    return f"{title}\n{border(border_char)}\n{_wrap(text, monospace)}"

def result_box(title, content, icon="📊", border_char="━"):
    """Kotak hasil dengan ikon dan border ganda."""
    return (
        f"{icon} **{title}**\n"
        f"{border(border_char)}\n"
        f"{content}\n"
        f"{border(border_char)}"
    )

def progress(current, total, length=10, fill="█", empty="░", monospace=True):
    """Progress bar sederhana."""
    percent = current / total
    filled = int(length * percent)
    bar = fill * filled + empty * (length - filled)
    text = f"[{bar}] {int(percent*100)}%"
    return f"`{text}`" if monospace else text

def list_items(items, title="📋 DAFTAR", numbered=False, empty_msg="_Tidak ada data_", border_char="━"):
    """Membuat daftar item rapi dengan border."""
    if not items:
        return f"{title}\n{border(border_char)}\n{empty_msg}\n{border(border_char)}"
    lines = []
    for i, item in enumerate(items, 1):
        prefix = f"{i}. " if numbered else "• "
        lines.append(f"{prefix}{item}")
    return f"{title}\n{border(border_char)}\n" + "\n".join(lines) + f"\n{border(border_char)}"

def status_report(success_count, fail_count, total=None, process_name="PROSES", border_char="━"):
    """Laporan status eksekusi dengan border."""
    if total is None:
        total = success_count + fail_count
    return result_box(
        f"HASIL {process_name.upper()}",
        f"✅ Berhasil: `{success_count}`\n❌ Gagal: `{fail_count}`\n📊 Total: `{total}`",
        icon="📈",
        border_char=border_char
    )

# Fungsi pembantu markdown (singkat)
def inline(text): return f"`{text}`"
def bold(text): return f"**{text}**"
def italic(text): return f"__{text}__"
def mono(text): return f"`{text}`"
def link(text, url): return f"[{text}]({url})"
