# modules/blacklist.py
from app import app
from pyrogram import filters
from pyrogram.enums import ChatType
import json
import os
import asyncio
from modules.styles import success, error, info, result_box

print("✅ Blacklist module loaded!")

BLACKLIST_FILE = "data/blacklist.json"

if not os.path.exists("data"):
    os.makedirs("data")

def get_blacklist():
    try:
        with open(BLACKLIST_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"groups": []}

def save_blacklist(data):
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.on_message(filters.command("bl", ".") & filters.me)
async def add_blacklist(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply(error("Harus di dalam grup!"))
        return
    
    bl = get_blacklist()
    chat_id = message.chat.id
    chat_title = message.chat.title or "Grup Tanpa Nama"
    
    if chat_id in bl["groups"]:
        await message.reply(error(f"{chat_title} sudah di blacklist"))
        return
    
    bl["groups"].append(chat_id)
    save_blacklist(bl)
    
    await message.reply(success(f"{chat_title} ditambahkan ke blacklist"))

@app.on_message(filters.command("unbl", ".") & filters.me)
async def del_blacklist(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply(error("Harus di dalam grup!"))
        return
    
    bl = get_blacklist()
    chat_id = message.chat.id
    chat_title = message.chat.title or "Grup Tanpa Nama"
    
    if chat_id not in bl["groups"]:
        await message.reply(error(f"{chat_title} tidak ada di blacklist"))
        return
    
    bl["groups"].remove(chat_id)
    save_blacklist(bl)
    
    await message.reply(success(f"{chat_title} dihapus dari blacklist"))

@app.on_message(filters.command("listbl", ".") & filters.me)
async def list_blacklist(client, message):
    bl = get_blacklist()
    
    if not bl["groups"]:
        await message.reply("📭 **Blacklist:** Belum ada grup")
        return
    
    text = ""
    for i, gid in enumerate(bl["groups"], 1):
        try:
            chat = await client.get_chat(gid)
            text += f"{i}. {chat.title} (ID: {gid})\n"
        except:
            text += f"{i}. Grup Tidak Dikenal (ID: {gid})\n"
    
    await message.reply(result_box("DAFTAR BLACKLIST", text, "📋"))

@app.on_message(filters.command("gcast", ".") & filters.me)
async def gcast_command(client, message):
    if not message.reply_to_message:
        await message.reply(error("Reply ke pesan yang mau di-GCAST!"))
        return
    
    text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        await message.reply(error("Pesan kosong!"))
        return
    
    status = await message.reply("📢 **Broadcast dimulai...**")
    
    sent = 0
    failed = 0
    skipped = 0
    
    bl = get_blacklist()
    blacklist = bl["groups"]
    
    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            if dialog.chat.id in blacklist:
                skipped += 1
                continue
            try:
                await client.send_message(dialog.chat.id, text)
                sent += 1
                await asyncio.sleep(1)
            except:
                failed += 1
    
    result = f"✅ Terkirim: {sent}\n⏭️ Di-skip: {skipped}\n❌ Gagal: {failed}"
    await status.edit(result_box("HASIL GCAST", result, "📊"))
