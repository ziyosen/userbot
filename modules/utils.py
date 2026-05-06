from app import app
from pyrogram import filters
import time
import os
import platform
from datetime import datetime
from modules.styles import result_box

print("✅ Utils module loaded!")

START_TIME = datetime.now()

def get_uptime():
    delta = datetime.now() - START_TIME
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

@app.on_message(filters.command("ping", ".") & filters.me)
async def ping_command(client, message):
    start = time.time()
    await message.edit("📡 **Pinging...**")
    end = time.time()
    ping_ms = round((end - start) * 1000)
    await message.edit(f"🚀 **Pong!!**\n⏱️ `Latency: {ping_ms}ms`\n🌐 `Status: Online`")

@app.on_message(filters.command("alive", ".") & filters.me)
async def alive_command(client, message):
    mod_count = len([f for f in os.listdir("modules") if f.endswith('.py')])
    dev_link = "[Bleszh](https://t.me/Bleszh)"
    
    content = (
        f"👤 **User:** {client.me.first_name}\n"
        f"👨‍💻 **Developer:** {dev_link}\n"
        f"⏱️ **Uptime:** `{get_uptime()}`\n"
        f"📦 **Modules:** `{mod_count} active`\n"
        f"🛡️ **Status:** `Protected`"
    )
    await message.edit(result_box("BENXX USERBOT ONLINE", content, "✨"))

@app.on_message(filters.command("help", ".") & filters.me)
async def help_command(client, message):
    help_text = (
        "👑 **ADMIN**: `ban, kick, mute, purge, del`\n"
        "🔍 **OSINT**: `ip, ipsakti, myip, cekno`\n"
        "🛠️ **TOOLS**: `stiker, emoji, whois`\n"
        "📊 **STATS**: `stats, sysinfo, botinfo`\n"
        "📦 **CORE**: `ping, alive, help`"
    )
    await message.edit(result_box("COMMAND LIST", help_text, "📖"))
