from app import app
from pyrogram import filters, enums
from pyrogram.enums import ChatType
import os
import asyncio

print("✅ Info module loaded!")

@app.on_message(filters.command("id", ".") & filters.me)
async def get_id(client, message):
    # Logika: Cek reply dulu
    if message.reply_to_message:
        target = message.reply_to_message.from_user or message.reply_to_message.sender_chat
        title = "USER" if hasattr(target, "first_name") else "CHANNEL/CHAT"
        name = getattr(target, "first_name", getattr(target, "title", "Unknown"))
        
        await message.edit(
            f"**🆔 ID {title}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Nama: **{name}**\n"
            f"🆔 ID: `{target.id}`"
        )
    
    # Logika: Cek Chat saat ini
    else:
        await message.edit(
            f"**🆔 INFO CHAT INI**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 Judul: **{message.chat.title or message.chat.first_name}**\n"
            f"🆔 ID: `{message.chat.id}`\n"
            f"👥 Tipe: `{message.chat.type.value}`"
        )

@app.on_message(filters.command("whois", ".") & filters.me)
async def whois_command(client, message):
    # Logika Target
    user_input = message.command[1] if len(message.command) > 1 else None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif user_input:
        user_id = user_input
    else:
        user_id = message.from_user.id

    status = await message.edit("🔄 **Mencari info...**")
    
    try:
        user = await client.get_users(user_id)
        full_user = await client.get_chat(user.id)
        
        teks = (
            f"**📋 WHOIS: {user.first_name}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **User ID:** `{user.id}`\n"
            f"🌐 **Username:** @{user.username or '-'}\n"
            f"📡 **DC ID:** {user.dc_id or 'Unknown'}\n"
            f"⭐ **Premium:** {'Ya' if getattr(user, 'is_premium', False) else 'Tidak'}\n"
            f"🤖 **Bot:** {'Ya' if user.is_bot else 'Bukan'}\n"
        )
        
        if full_user.bio:
            teks += f"📝 **Bio:** `{full_user.bio}`\n"
        
        teks += f"━━━━━━━━━━━━━━━━━━━━━━━"

        # Cek Foto
        if user.photo:
            await client.send_photo(message.chat.id, user.photo.big_file_id, caption=teks)
            await status.delete()
        else:
            await status.edit(teks)
            
    except Exception as e:
        await status.edit(f"❌ **Error:** `{e}`")

@app.on_message(filters.command("info", ".") & filters.me)
async def info_grup(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.edit("❌ Harus di dalam grup!")
    
    status = await message.edit("🔄 **Mengambil info grup...**")
    
    try:
        full = await client.get_chat(message.chat.id)
        members_count = await client.get_chat_members_count(message.chat.id)
        
        teks = (
            f"**📊 INFO GRUP: {full.title}**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **ID Grup:** `{full.id}`\n"
            f"👥 **Anggota:** `{members_count}`\n"
            f"🌐 **Username:** @{full.username or '-'}\n"
            f"🎤 **VC Aktif:** {'Ya' if full.is_voice_chat_started else 'Tidak'}\n"
        )

        if full.photo:
            # Pake send_photo langsung dengan file_id biar hemat kuota Termux
            await client.send_photo(message.chat.id, full.photo.big_file_id, caption=teks)
            await status.delete()
        else:
            await status.edit(teks)
            
    except Exception as e:
        await status.edit(f"❌ **Error:** `{e}`")
