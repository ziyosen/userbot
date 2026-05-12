import asyncio
import json
import os
from app import app  # ← perubahan utama: import app
from pyrogram import filters, enums
from pyrogram.enums import ChatType, ChatMemberStatus

# --- KONFIGURASI DATABASE ---
BLACKLIST_FILE = "data/blacklist.json"
if not os.path.exists("data"):
    os.makedirs("data")

def get_blacklist():
    try:
        with open(BLACKLIST_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"groups": []}

def save_blacklist(data):
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- MODUL ADMIN ---

@app.on_message(filters.command("adminlist", ".") & filters.me)  # ← @app
async def adminlist_handler(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.edit("❌ Fitur ini hanya untuk Grup!")
    
    await message.edit("🔍 **Mengambil daftar admin...**")
    out_str = f"🛡️ **ADMIN LIST: {message.chat.title}**\n\n"
    owner = ""
    admins = []

    try:
        async for m in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            name = m.user.first_name if not m.user.is_deleted else "Akun Terhapus"
            if m.status == ChatMemberStatus.OWNER:
                owner = f"👑 **Owner:** [{name}](tg://user?id={m.user.id})\n"
            else:
                admins.append(f"🪯 [{name}](tg://user?id={m.user.id})")
        
        await message.edit(owner + "\n".join(admins))
    except Exception as e:
        await message.edit(f"❌ **Gagal:** `{e}`")

@app.on_message(filters.command(["ban", "kick", "unban"], ".") & filters.me)
async def moderation_handler(client, message):
    cmd = message.command[0]
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.edit("❌ Gunakan di dalam grup!")

    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]

    if not user_id:
        return await message.edit(f"❓ Mau di-{cmd} siapa? Reply atau masukan ID.")

    try:
        if cmd == "ban":
            await client.ban_chat_member(message.chat.id, user_id)
            await message.edit(f"✅ User `{user_id}` di-**BAN**.")
        elif cmd == "kick":
            await client.ban_chat_member(message.chat.id, user_id)
            await client.unban_chat_member(message.chat.id, user_id)
            await message.edit(f"✅ User `{user_id}` di-**KICK**.")
        elif cmd == "unban":
            await client.unban_chat_member(message.chat.id, user_id)
            await message.edit(f"✅ User `{user_id}` di-**UNBAN**.")
    except Exception as e:
        await message.edit(f"❌ **Gagal:** `{e}`")

# --- MODULE BLACKLIST & GCAST ---

@app.on_message(filters.command(["bl", "unbl"], ".") & filters.me)
async def blacklist_logic(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return await message.edit("❌ Harus di dalam grup!")
    
    cmd = message.command[0]
    bl = get_blacklist()
    chat_id = message.chat.id
    chat_title = message.chat.title

    if cmd == "bl":
        if chat_id in bl["groups"]:
            return await message.edit(f"ℹ️ `{chat_title}` sudah di blacklist.")
        bl["groups"].append(chat_id)
        save_blacklist(bl)
        await message.edit(f"✅ `{chat_title}` ditambahkan ke blacklist.")
    else:
        if chat_id not in bl["groups"]:
            return await message.edit(f"ℹ️ `{chat_title}` tidak ada di blacklist.")
        bl["groups"].remove(chat_id)
        save_blacklist(bl)
        await message.edit(f"✅ `{chat_title}` dihapus dari blacklist.")

@app.on_message(filters.command("gcast", ".") & filters.me)
async def gcast_improved(client, message):
    msg = message.reply_to_message if message.reply_to_message else None
    
    if not msg and len(message.command) < 2:
        return await message.edit("❌ Reply ke pesan atau ketik teks untuk GCAST!")

    status = await message.edit("📢 **Broadcast dimulai...**")
    sent, failed, skipped = 0, 0, 0
    blacklist = get_blacklist()["groups"]

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            if dialog.chat.id in blacklist:
                skipped += 1
                continue
            try:
                if msg:
                    await msg.copy(dialog.chat.id)
                else:
                    text_to_send = message.text.split(None, 1)[1]
                    await client.send_message(dialog.chat.id, text_to_send)
                sent += 1
                await asyncio.sleep(0.5)
            except Exception:
                failed += 1

    await status.edit(
        f"📊 **HASIL GCAST**\n"
        f"━━━━━━━━━━━━━━\n"
        f"✅ Terkirim: `{sent}`\n"
        f"⏭️ Di-skip: `{skipped}`\n"
        f"❌ Gagal: `{failed}`"
    )
