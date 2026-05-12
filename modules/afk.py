from app import app
from pyrogram import filters
from pyrogram.types import Message
import asyncio
import time
import os
from datetime import datetime

# ========== GLOBAL STATE ==========
AFK_STATUS = False
AFK_REASON = ""
AFK_MEDIA = None          # (file_id, media_type)
AFK_START_TIME = 0.0
AFK_REPLIED_CHATS = set()

# ========== FUNGSI BANTU ==========
def get_media_info(msg: Message):
    """Ekstrak file_id dan tipe media dari pesan yang di-reply."""
    if msg.sticker:
        return (msg.sticker.file_id, "sticker")
    elif msg.photo:
        return (msg.photo.file_id, "photo")
    elif msg.animation:
        return (msg.animation.file_id, "animation")
    elif msg.video:
        return (msg.video.file_id, "video")
    elif msg.voice:
        return (msg.voice.file_id, "voice")
    elif msg.audio:
        return (msg.audio.file_id, "audio")
    elif msg.document and msg.document.mime_type and "image" in msg.document.mime_type:
        return (msg.document.file_id, "photo")
    return None

async def send_media_or_text(client, chat_id, text, media_info):
    """Kirim pesan (dengan media jika ada)."""
    if not media_info:
        return await client.send_message(chat_id, text)
    file_id, media_type = media_info
    if media_type == "sticker":
        return await client.send_sticker(chat_id, file_id)
    elif media_type == "photo":
        return await client.send_photo(chat_id, file_id, caption=text)
    elif media_type == "animation":
        return await client.send_animation(chat_id, file_id, caption=text)
    elif media_type == "video":
        return await client.send_video(chat_id, file_id, caption=text)
    elif media_type == "voice":
        return await client.send_voice(chat_id, file_id, caption=text)
    elif media_type == "audio":
        return await client.send_audio(chat_id, file_id, caption=text)
    else:
        return await client.send_message(chat_id, text)

# ========== PERINTAH .afk ==========
@app.on_message(filters.command("afk", ".") & filters.me)
async def set_afk(client, message: Message):
    global AFK_STATUS, AFK_REASON, AFK_MEDIA, AFK_START_TIME, AFK_REPLIED_CHATS
    
    # Ambil alasan (setelah .afk)
    reason = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    media_info = None
    if message.reply_to_message:
        media_info = get_media_info(message.reply_to_message)
    
    # Aktifkan AFK
    AFK_STATUS = True
    AFK_REASON = reason
    AFK_MEDIA = media_info
    AFK_START_TIME = time.time()
    AFK_REPLIED_CHATS.clear()
    
    # Hapus pesan perintah
    await message.delete()
    
    # Kirim konfirmasi
    confirm_text = "🔴 **Mode AFK diaktifkan.**"
    if reason:
        confirm_text += f"\n📝 **Alasan:** `{reason}`"
    if media_info:
        confirm_text += "\n📎 **Media akan dikirim saat dibalas.**"
    await client.send_message(message.chat.id, confirm_text)

# ========== AUTO DEACTIVATE AFK SAAT OWNER KIRIM PESAN (selain perintah .afk) ==========
@app.on_message(filters.me & ~filters.command("afk", "."))
async def auto_deactivate_afk(client, message: Message):
    global AFK_STATUS, AFK_START_TIME, AFK_REASON, AFK_MEDIA, AFK_REPLIED_CHATS
    if not AFK_STATUS:
        return
    
    # Hitung durasi AFK
    dur = int(time.time() - AFK_START_TIME)
    if dur < 60:
        dur_str = f"{dur} detik"
    elif dur < 3600:
        minutes = dur // 60
        seconds = dur % 60
        dur_str = f"{minutes} menit {seconds} detik"
    else:
        hours = dur // 3600
        minutes = (dur % 3600) // 60
        dur_str = f"{hours} jam {minutes} menit"
    
    # Matikan AFK
    AFK_STATUS = False
    AFK_REASON = ""
    AFK_MEDIA = None
    AFK_REPLIED_CHATS.clear()
    
    # Kirim notifikasi kembali online
    await client.send_message(
        message.chat.id,
        f"✅ **Kembali online!**\n⏱️ AFK selama: `{dur_str}`"
    )

# ========== BALAS OTOMATIS SAAT DIMENSI / PM ==========
@app.on_message(filters.incoming & ~filters.me & (filters.private | filters.mentioned) & ~filters.bot)
async def auto_reply_afk(client, message: Message):
    global AFK_STATUS, AFK_REASON, AFK_START_TIME, AFK_MEDIA, AFK_REPLIED_CHATS
    if not AFK_STATUS:
        return
    
    chat_id = message.chat.id
    # Hanya balas sekali per chat
    if chat_id in AFK_REPLIED_CHATS:
        return
    AFK_REPLIED_CHATS.add(chat_id)
    
    # Hitung durasi
    dur = int(time.time() - AFK_START_TIME)
    if dur < 60:
        dur_str = f"{dur} detik"
    elif dur < 3600:
        minutes = dur // 60
        seconds = dur % 60
        dur_str = f"{minutes} menit {seconds} detik"
    else:
        hours = dur // 3600
        minutes = (dur % 3600) // 60
        dur_str = f"{hours} jam {minutes} menit"
    
    me = await client.get_me()
    owner_name = me.first_name
    if AFK_REASON:
        reply_text = (
            f"🔴 **{owner_name} sedang AFK**\n"
            f"⏱️ Sejak: `{dur_str}` yang lalu\n"
            f"📝 **Alasan:** {AFK_REASON}"
        )
    else:
        reply_text = (
            f"🔴 **{owner_name} sedang AFK**\n"
            f"⏱️ Sejak: `{dur_str}` yang lalu"
        )
    
    await send_media_or_text(client, chat_id, reply_text, AFK_MEDIA)
