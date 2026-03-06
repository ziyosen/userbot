# modules/system_stats.py
from app import app
from pyrogram import filters
import platform
import os
from datetime import datetime

print("✅ System Stats module loaded!")

START_TIME = datetime.now()

@app.on_message(filters.command("stats", ".") & filters.me)
async def bot_stats(client, message):
    status = await message.reply("📊 **Menghitung statistik...**")
    
    total_chats = 0
    total_groups = 0
    total_channels = 0
    total_users = 0
    total_bots = 0
    
    async for dialog in client.get_dialogs():
        total_chats += 1
        if dialog.chat.type == "group" or dialog.chat.type == "supergroup":
            total_groups += 1
        elif dialog.chat.type == "channel":
            total_channels += 1
        elif dialog.chat.type == "private":
            if dialog.chat.is_bot:
                total_bots += 1
            else:
                total_users += 1
    
    now = datetime.now()
    uptime = now - START_TIME
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    
    header = "📊 **USERBOT STATISTICS**\n\n"
    content = (
        "```"
        f"⏱️ Uptime   : {days}h {hours}j {minutes}m\n"
        f"🐍 Python   : {platform.python_version()}\n"
        f"💬 Total    : {total_chats}\n"
        f"👥 Grup     : {total_groups}\n"
        f"📢 Channel  : {total_channels}\n"
        f"👤 User PM  : {total_users}\n"
        f"🤖 Bot PM   : {total_bots}"
        "```"
    )
    
    await status.edit(header + content)

@app.on_message(filters.command("sysinfo", ".") & filters.me)
async def system_info(client, message):
    try:
        import psutil
        disk = psutil.disk_usage('/')
        disk_total = disk.total / (1024**3)
        disk_used = disk.used / (1024**3)
        disk_percent = disk.percent
        
        header = "💻 **SISTEM INFORMASI**\n\n"
        content = (
            "```"
            f"> Platform : {platform.system()} {platform.release()}\n"
            f"> Arch     : {platform.machine()}\n"
            f"> Host     : {platform.node()}\n"
            f"> Storage  : {disk_used:.2f}GB/{disk_total:.2f}GB ({disk_percent}%)"
            "```"
        )
        
        await message.reply(header + content)
        
    except:
        statvfs = os.statvfs('/')
        total = statvfs.f_frsize * statvfs.f_blocks / (1024**3)
        free = statvfs.f_frsize * statvfs.f_bfree / (1024**3)
        used = total - free
        percent = (used / total) * 100
        
        header = "💻 **SISTEM INFORMASI**\n\n"
        content = (
            "```"
            f"> Platform : {platform.system()} {platform.release()}\n"
            f"> Arch     : {platform.machine()}\n"
            f"> Host     : {platform.node()}\n"
            f"> Storage  : {used:.2f}GB/{total:.2f}GB ({percent:.1f}%)"
            "```"
        )
        
        await message.reply(header + content)

@app.on_message(filters.command("botinfo", ".") & filters.me)
async def bot_info(client, message):
    me = await client.get_me()
    
    now = datetime.now()
    uptime = now - START_TIME
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    
    modules_dir = "modules"
    module_count = len([f for f in os.listdir(modules_dir) if f.endswith('.py') and f != '__init__.py'])
    
    header = "🤖 **BOT INFORMATION**\n\n"
    content = (
        "```"
        f"⏱️ Uptime   : {days}h {hours}j {minutes}m\n"
        f"📦 Modules  : {module_count}\n"
        f"🐍 Python   : {platform.python_version()}\n"
        f"👤 Nama     : {me.first_name} {me.last_name or ''}\n"
        f"🆔 ID       : {me.id}\n"
        f"🌐 Username : @{me.username if me.username else '-'}"
        "```"
    )
    
    await message.reply(header + content)
