# modules/utils.py
from app import app
from pyrogram import filters
import time
import platform
from datetime import datetime

print("✅ Utils module loaded!")

START_TIME = datetime.now()

@app.on_message(filters.command("ping", ".") & filters.me)
async def ping_command(client, message):
    start = time.time()
    msg = await message.reply("📡 **Pinging...**")
    end = time.time()
    ping_ms = round((end - start) * 1000)
    await msg.edit(f"📡 **Pong!** `{ping_ms}ms`")

@app.on_message(filters.command("alive", ".") & filters.me)
async def alive_command(client, message):
    # Hitung uptime
    now = datetime.now()
    uptime = now - START_TIME
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    
    # Hitung modules
    import os
    modules_dir = "modules"
    module_count = len([f for f in os.listdir(modules_dir) if f.endswith('.py') and f != '__init__.py'])
    
    # SEMUA DALAM 1 BLOCK CODE
    text = (
        "```"
        "AKEO USERBOT\n"
        f"Uptime: {days}h {hours}j {minutes}m\n"
        "Status: Online\n"
        f"Python: {platform.python_version()}\n"
        f"Modules: {module_count}\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "        DAFTAR COMMANDS     \n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "\n"
        "📦 CORE\n"
        "  .ping  .alive  .uptime\n"
        "\n"
        "🚫 BLACKLIST\n"
        "  .bl  .unbl  .listbl  .gcast\n"
        "\n"
        "👑 ADMIN\n"
        "  .ban  .kick  .unban  .mute\n"
        "  .unmute  .del  .purge\n"
        "  .settitle  .setphoto\n"
        "  .adminlist  .promote  .demote\n"
        "\n"
        "🛠️ TOOLS\n"
        "  .stiker  .emoji  .id\n"
        "  .whois  .info\n"
        "\n"
        "🔍 OSINT\n"
        "  .ip  .ipsakti  .myip\n"
        "  .sherlock  .cekno\n"
        "\n"
        "📊 SYSTEM\n"
        "  .stats  .sysinfo  .botinfo\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Total: {module_count} Modules Active\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━"
        "```"
    )
    
    await message.reply(text)

@app.on_message(filters.command("uptime", ".") & filters.me)
async def uptime_command(client, message):
    now = datetime.now()
    uptime = now - START_TIME
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    seconds = uptime.seconds % 60
    
    await message.reply(
        f"**⏱️ System Uptime**\n"
        f"📅 `{days} hari`\n"
        f"⏰ `{hours} jam {minutes} menit {seconds} detik`"
    )
