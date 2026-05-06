from pyrogram import filters
from app import app
import asyncio

@app.on_message(filters.command("gcast", ".") & filters.me)
async def gcast_cmd(client, message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.edit("<b>Berikan pesan atau reply pesan untuk Gcast!</b>")

    msg = message.reply_to_message if message.reply_to_message else message.text.split(None, 1)[1]
    await message.edit("🚀 **Memulai Global Broadcast...**")
    
    done = 0
    failed = 0
    
    async for dialog in client.get_dialogs():
        if dialog.chat.type in ["group", "supergroup"]:
            try:
                if message.reply_to_message:
                    await msg.copy(dialog.chat.id)
                else:
                    await client.send_message(dialog.chat.id, msg)
                done += 1
                await asyncio.sleep(0.3) # Jeda dikit biar gak kena spam limit
            except Exception:
                failed += 1

    await message.edit(f"✅ **Gcast Selesai!**\n\n Berhasil: `{done}` Grup\n Gagal: `{failed}` Grup")
