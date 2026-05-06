from pyrogram import filters
from pyrogram.enums import ChatType
from app import app
import asyncio

@app.on_message(filters.command("gcast", ".") & filters.me)
async def gcast_cmd(client, message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.edit("<b>Berikan pesan atau reply pesan untuk Gcast!</b>")

    # Ambil konten pesan
    if message.reply_to_message:
        msg = message.reply_to_message
    else:
        msg = message.text.split(None, 1)[1]

    await message.edit("🚀 **Memulai Global Broadcast...**")
    
    done = 0
    failed = 0
    
    # Ambil semua dialog (chat yang aktif di akunmu)
    async for dialog in client.get_dialogs():
        # Cek apakah tipe chat adalah Grup atau Supergroup
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            try:
                if message.reply_to_message:
                    await msg.copy(dialog.chat.id)
                else:
                    await client.send_message(dialog.chat.id, msg)
                
                done += 1
                # Delay 0.5 detik agar tidak terkena mute/floodwait oleh Telegram
                await asyncio.sleep(0.5) 
            except Exception:
                failed += 1

    await message.edit(
        f"✅ **Gcast Selesai!**\n\n"
        f"👤 **Target:** Grup & Supergroup\n"
        f"🎉 **Berhasil:** `{done}`\n"
        f"❌ **Gagal:** `{failed}`"
    )
