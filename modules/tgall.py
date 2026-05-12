# modules/tagger.py
from app import app
from pyrogram import filters, enums
from pyrogram.types import Message
import asyncio
import random

# Daftar emoji (salin dari kode asli - cukup banyak)
EMOJI_LIST = [
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😭", "😗", "😙", "😚", "😘", "🥰", "😍",
    "🤩", "🥳", "🤗", "🙃", "🙂", "☺️", "😊", "😏", "😌", "😉", "🤭", "😶", "😐", "😑", "😔",
    "😋", "😛", "😝", "😜", "🤪", "🤔", "🤨", "🧐", "🙄", "😒", "😤", "😠", "🤬", "☹️", "🙁",
    "😕", "😟", "🥺", "😳", "😬", "🤐", "🤫", "😰", "😨", "😧", "😦", "😮", "😯", "😲", "😱",
    "🤯", "😢", "😥", "😓", "😞", "😖", "😣", "😩", "😫", "🤤", "🥱", "😴", "😪", "🌛", "🌜",
    "🎲", "🧩", "♟", "🎯", "🎳", "🎭", "💕", "💞", "💓", "💗", "💖", "❤️‍🔥", "💔", "🤎", "🤍",
    "🖤", "❤️", "🧡", "💛", "💚", "💙", "💜", "💘", "💝", "🐵", "🦁", "🐯", "🐱", "🐶", "🐺",
    "🐻", "🐨", "🐼", "🐹", "🐭", "🐰", "🦊", "🦝", "🐮", "🐷", "🐽", "🐗", "🦓", "🦄", "🐴",
    "🐸", "🐲", "🦎", "🐉", "🦖", "🦕", "🐢", "🐊", "🐍", "🐁", "🐀", "🐇", "🐈", "🐩", "🐕",
    "🦮", "🐕‍🦺", "🐅", "🐆", "🐎", "🐖", "🐄", "🐂", "🐃", "🐏", "🐑", "🐐", "🦌", "🦙", "🦥",
    "🦘", "🐘", "🦏", "🦛", "🦒", "🐒", "🦍", "🦧", "🐪", "🐫", "🐿️", "🦨", "🦡", "🦔", "🦦",
    "🦇", "🐓", "🐔", "🐣", "🐤", "🐥", "🐦", "🦉", "🦅", "🦜", "🕊️", "🦢", "🦩", "🦚", "🦃",
    "🦆", "🐧", "🦈", "🐬", "🐋", "🐳", "🐟", "🐠", "🐡", "🦐", "🦞", "🦀", "🦑", "🐙", "🦪",
    "🦂", "🕷️", "🦋", "🐞", "🐝", "🦟", "🦗", "🐜", "🐌", "🐚", "🕸️", "🐛", "🐾", "🌞", "🤢",
    "🤮", "🤧", "🤒", "🍓", "🍒", "🍎", "🍉", "🍑", "🍊", "🥭", "🍍", "🍌", "🌶", "🍇", "🥝",
    "🍐", "🍏", "🍈", "🍋", "🍄", "🥕", "🍠", "🧅", "🌽", "🥦", "🥒", "🥬", "🥑", "🥯", "🥖",
    "🥐", "🍞", "🥜", "🌰", "🥔", "🧄", "🍆", "🧇", "🥞", "🥚", "🧀", "🥓", "🥩", "🍗", "🍖",
    "🥙", "🌯", "🌮", "🍕", "🍟", "🥨", "🥪", "🌭", "🍔", "🧆", "🥘", "🍝", "🥫", "🥣", "🥗",
    "🍲", "🍛", "🍜", "🍢", "🥟", "🍱", "🍚", "🥡", "🍤", "🍣", "🦞", "🦪", "🍘", "🍡", "🥠",
    "🥮", "🍧", "🍨"
]

# Flag untuk menghentikan proses (per chat)
stop_flag = {}

def get_stop_flag(chat_id: int) -> bool:
    return stop_flag.get(chat_id, False)

def set_stop_flag(chat_id: int, value: bool):
    stop_flag[chat_id] = value

# ========== .mention ==========
@app.on_message(filters.command("mention", ".") & filters.me)
async def mention_all(client, message: Message):
    """Tag semua anggota dengan @all (tanpa nama)."""
    chat_id = message.chat.id
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit("❌ Perintah ini hanya untuk grup.")
    
    await message.delete()
    text = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    # Ambil anggota non-bot
    members = []
    async for member in client.get_chat_members(chat_id):
        if not member.user.is_bot:
            members.append(member.user.id)
    if not members:
        return await client.send_message(chat_id, "❌ Tidak ada anggota non-bot.")
    
    sent = await client.send_message(chat_id, f"@all {text}\n" if text else "@all")
    # Kirim tag per 5 orang
    for i in range(0, len(members), 5):
        batch = members[i:i+5]
        tags = " ".join([f"[\u2063](tg://user?id={uid})" for uid in batch])
        if text:
            tags += f" {text}"
        await client.send_message(chat_id, tags)
        await asyncio.sleep(1)
    await sent.delete()

# ========== .tagall (dari command .all di versi asli) ==========
@app.on_message(filters.command("tagall", ".") & filters.me)
async def tag_all_name(client, message: Message):
    """Tag semua anggota dengan nama mereka (per 5 per pesan)."""
    chat_id = message.chat.id
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit("❌ Hanya untuk grup.")
    
    await message.delete()
    text = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    set_stop_flag(chat_id, False)
    status_msg = await client.send_message(chat_id, "🚀 Memulai tag all... (`.stop` untuk berhenti)")
    
    # Kumpulkan anggota non-bot
    members = []
    async for m in client.get_chat_members(chat_id):
        if not m.user.is_bot:
            members.append(m.user)
    if not members:
        await status_msg.edit("❌ Tidak ada anggota non-bot.")
        return
    
    for i in range(0, len(members), 5):
        if get_stop_flag(chat_id):
            await client.send_message(chat_id, "⏹️ Tag all dihentikan.")
            break
        batch = members[i:i+5]
        msg_text = ""
        for u in batch:
            name = u.first_name or u.username or "User"
            msg_text += f"👤 [{name}](tg://user?id={u.id})\n"
        if text:
            msg_text += f"\n{text}"
        await client.send_message(chat_id, msg_text)
        await asyncio.sleep(1.5)
    else:
        await client.send_message(chat_id, "✅ Tag all selesai.")
    await status_msg.delete()
    set_stop_flag(chat_id, False)

# ========== .emojitag ==========
@app.on_message(filters.command("emojitag", ".") & filters.me)
async def emoji_tag(client, message: Message):
    """Tag semua anggota dengan emoji random (per 5 per pesan)."""
    chat_id = message.chat.id
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.edit("❌ Hanya untuk grup.")
    
    await message.delete()
    text = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    set_stop_flag(chat_id, False)
    status_msg = await client.send_message(chat_id, "🎭 Memulai emoji tag... (`.stop` untuk berhenti)")
    
    members = []
    async for m in client.get_chat_members(chat_id):
        if not m.user.is_bot:
            members.append(m.user)
    if not members:
        await status_msg.edit("❌ Tidak ada anggota non-bot.")
        return
    
    for i in range(0, len(members), 5):
        if get_stop_flag(chat_id):
            await client.send_message(chat_id, "⏹️ Emoji tag dihentikan.")
            break
        batch = members[i:i+5]
        tags = []
        for u in batch:
            em = random.choice(EMOJI_LIST)
            tags.append(f"[{em}](tg://user?id={u.id})")
        if text:
            tags.append(text)
        await client.send_message(chat_id, " ".join(tags))
        await asyncio.sleep(1)
    else:
        await client.send_message(chat_id, "✅ Emoji tag selesai.")
    await status_msg.delete()
    set_stop_flag(chat_id, False)

# ========== .stop (menghentikan proses tag all atau emojitag) ==========
@app.on_message(filters.command("stop", ".") & filters.me)
async def stop_tagging(client, message: Message):
    chat_id = message.chat.id
    set_stop_flag(chat_id, True)
    await message.edit("🛑 Perintah stop diterima, tag akan berhenti.")
    await asyncio.sleep(2)
    await message.delete()
