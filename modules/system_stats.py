from app import app
from pyrogram import filters
import platform
import os
import time
from datetime import datetime
from modules.styles import result_box, info

print("✅ System Stats module loaded!")

# Catat waktu mulai dalam format timestamp biar lebih akurat
START_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

@app.on_message(filters.command("stats", ".") & filters.me)
async def bot_stats(client, message):
    status = await message.edit("📊 **Sedang menghitung data...**")
    
    # Inisialisasi counter
    c = {"total": 0, "groups": 0, "channels": 0, "users": 0, "bots": 0}
    
    # Gunakan limit jika chat terlalu banyak biar Termux gak crash
    async for dialog in client.get_dialogs():
        c["total"] += 1
        dtype = dialog.chat.type
        if dtype in ["group", "supergroup"]:
            c["groups"] += 1
        elif dtype == "channel":
            c["channels"] += 1
        elif dtype == "private":
            if dialog.chat.is_bot: c["bots"] += 1
            else: c["users"] += 1

    uptime = get_readable_time(int(time.time() - START_TIME))
    
    res = (
        f"⏱️ **Uptime:** `{uptime}`\n"
        f"💬 **Total Chat:** `{c['total']}`\n"
        f"👥 **Grup:** `{c['groups']}`\n"
        f"📢 **Channel:** `{c['channels']}`\n"
        f"👤 **User:** `{c['users']}`\n"
        f"🤖 **Bot:** `{c['bots']}`"
    )
    await status.edit(result_box("STATISTIK AKUN", res, "📊"))

@app.on_message(filters.command("sysinfo", ".") & filters.me)
async def system_info(client, message):
    await message.edit("📡 **Mengambil informasi server...**")
    
    # Logika Storage (Termux friendly)
    statvfs = os.statvfs('/')
    total = statvfs.f_frsize * statvfs.f_blocks / (1024**3)
    free = statvfs.f_frsize * statvfs.f_bfree / (1024**3)
    used = total - free
    percent = (used / total) * 100
    
    # Bikin bar penyimpanan sederhana [■■■□□]
    bar_size = 10
    filled = int(percent / 10)
    bar = "■" * filled + "□" * (bar_size - filled)

    res = (
        f"🖥️ **OS:** `{platform.system()} {platform.machine()}`\n"
        f"🐍 **Python:** `{platform.python_version()}`\n"
        f"🏠 **Node:** `{platform.node()}`\n\n"
        f"💾 **Storage:** `{percent:.1f}%`\n"
        f"`[{bar}]`\n"
        f"`{used:.2f}GB / {total:.2f}GB`"
    )
    await message.edit(result_box("SISTEM INFO", res, "💻"))

@app.on_message(filters.command("botinfo", ".") & filters.me)
async def bot_info(client, message):
    me = await client.get_me()
    uptime = get_readable_time(int(time.time() - START_TIME))
    
    # Hitung jumlah file di folder modules
    mod_count = len([f for f in os.listdir("modules") if f.endswith('.py')])

    res = (
        f"🤖 **Nama:** {me.first_name}\n"
        f"🆔 **ID:** `{me.id}`\n"
        f"📦 **Modules:** `{mod_count} file`\n"
        f"⏱️ **Uptime:** `{uptime}`\n"
        f"🔗 **User:** @{me.username if me.username else 'N/A'}"
    )
    await message.edit(result_box("BOT INFORMATION", res, "🤖"))
