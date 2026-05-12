from app import app
from pyrogram import filters
from pyrogram.enums import ChatType
import asyncio
import json
import os

# --- BLACKLIST (sama seperti di modul blacklist) ---
BLACKLIST_FILE = "data/blacklist.json"
if not os.path.exists("data"):
    os.makedirs("data")

def get_blacklist():
    try:
        with open(BLACKLIST_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"groups": []}

@app.on_message(filters.command("gcast", ".") & filters.me)
async def gcast_cmd(client, message):
    # Validasi: harus reply atau ada teks
    if not message.reply_to_message and len(message.command) < 2:
        return await message.edit("❌ **Reply ke pesan atau ketik teks setelah .gcast!**")

    # Ambil konten pesan
    if message.reply_to_message:
        content = message.reply_to_message
    else:
        content = message.text.split(None, 1)[1]

    status = await message.edit("🚀 **Memulai Global Broadcast...**")
    
    sent = 0
    failed = 0
    skipped = 0
    blacklist = get_blacklist()["groups"]
    
    async for dialog in client.get_dialogs():
        chat = dialog.chat
        # Kirim hanya ke Grup dan Supergrup
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            continue
        
        # Lewati grup yang ada di blacklist
        if chat.id in blacklist:
            skipped += 1
            continue
        
        try:
            if message.reply_to_message:
                await content.copy(chat.id)
            else:
                await client.send_message(chat.id, content)
            sent += 1
            await asyncio.sleep(0.5)  # hindari flood
        except Exception:
            failed += 1

    await status.edit(
        f"✅ **GCAST SELESAI**\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Berhasil: `{sent}`\n"
        f"⏭️ Di-skip (blacklist): `{skipped}`\n"
        f"❌ Gagal: `{failed}`"
    )
