# modules/styles.py
def success(text, title="BERHASIL"):
    return f"✅ **{title}:** {text}"

def error(text, title="GAGAL"):
    return f"❌ **{title}:** {text}"

def info(text, title="INFO"):
    return f"ℹ️ **{title}:** {text}"

def result_box(title, content, icon="📊"):
    return f"{icon} **{title}**\n{content}"
