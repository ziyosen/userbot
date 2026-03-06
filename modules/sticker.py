# modules/sticker.py
from app import app
from pyrogram import filters
from pyrogram.types import Message
import os
from PIL import Image
import time

print("✅ Sticker module loaded!")

@app.on_message(filters.command("stiker", ".") & filters.me)
async def to_sticker(client, message: Message):
    """Ubah gambar jadi stiker"""
    if not message.reply_to_message:
        await message.reply("❌ Reply ke gambar!")
        return
    
    # Cek apa yang di-reply
    msg = message.reply_to_message
    
    # Kalo reply ke sticker
    if msg.sticker:
        await message.reply("❌ Ini udah stiker bos!")
        return
    
    # Kalo reply ke foto
    if msg.photo:
        status = await message.reply("🔄 **Membuat stiker...**")
        
        # Download foto
        photo_path = await msg.download()
        
        # Buat nama file stiker
        stiker_path = f"stiker_{int(time.time())}.webp"
        
        # Convert ke stiker pake PIL
        try:
            img = Image.open(photo_path)
            # Resize stiker (max 512px)
            img.thumbnail((512, 512))
            # Simpan sebagai webp
            img.save(stiker_path, "WEBP")
            
            # Kirim sebagai stiker
            await client.send_sticker(message.chat.id, stiker_path)
            
            # Hapus file
            os.remove(photo_path)
            os.remove(stiker_path)
            
            await status.delete()
            
        except Exception as e:
            await status.edit(f"❌ Error: {e}")
            if os.path.exists(photo_path):
                os.remove(photo_path)
    
    # Kalo reply ke dokumen gambar
    elif msg.document and msg.document.mime_type and msg.document.mime_type.startswith("image/"):
        status = await message.reply("🔄 **Membuat stiker...**")
        
        # Download file
        file_path = await msg.download()
        
        stiker_path = f"stiker_{int(time.time())}.webp"
        
        try:
            img = Image.open(file_path)
            img.thumbnail((512, 512))
            img.save(stiker_path, "WEBP")
            
            await client.send_sticker(message.chat.id, stiker_path)
            
            os.remove(file_path)
            os.remove(stiker_path)
            
            await status.delete()
            
        except Exception as e:
            await status.edit(f"❌ Error: {e}")
            if os.path.exists(file_path):
                os.remove(file_path)
    
    else:
        await message.reply("❌ Itu bukan gambar bos!")

@app.on_message(filters.command("stikerpack", ".") & filters.me)
async def sticker_pack(client, message: Message):
    """Buat stiker pack dari beberapa gambar (reply ke 2+ gambar)"""
    if not message.reply_to_message:
        await message.reply("❌ Reply ke gambar pertama!")
        return
    
    # Cari semua gambar yang di-reply
    gambar_list = []
    msg = message.reply_to_message
    
    # Kalo reply ke pesan yang punya banyak media
    if msg.media_group_id:
        # Lagi ribet nih, tapi simple aja dulu
        await message.reply("⚠️ Fitur ini masih development")
        return
    else:
        await message.reply("📌 **Cara pake:**\nReply ke gambar & ketik .stiker")

@app.on_message(filters.command("emoji", ".") & filters.me)
async def text_to_emoji(client, message: Message):
    """Ubah teks jadi emoji (kasar)"""
    if len(message.command) < 2:
        await message.reply("❌ Pake: .emoji [teks]")
        return
    
    teks = " ".join(message.command[1:]).lower()
    
    # Mapping huruf ke emoji (sederhana)
    mapping = {
        'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪',
        'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯',
        'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴',
        'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹',
        'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾',
        'z': '🇿', ' ': '  ', '?': '❓', '!': '❗', '.': '⏺️'
    }
    
    hasil = ""
    for huruf in teks:
        hasil += mapping.get(huruf, huruf) + " "
    
    await message.reply(hasil)
