# modules/info.py
from app import app  # <-- INI YANG LO LUPA!
from pyrogram import filters
from pyrogram.enums import ChatType
import os

print("✅ Info module loaded!")

@app.on_message(filters.command("id", ".") & filters.me)
async def get_id(client, message):
    """Lihat ID user/grup"""
    
    # Kalo reply ke pesan
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        reply_text = f"**🆔 ID USER**\n"
        reply_text += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        reply_text += f"👤 Nama: **{user.first_name}**"
        if user.last_name:
            reply_text += f" {user.last_name}"
        reply_text += f"\n"
        reply_text += f"🆔 User ID: `{user.id}`\n"
        if user.username:
            reply_text += f"👤 Username: @{user.username}"
        else:
            reply_text += f"👤 Username: -"
        await message.reply(reply_text)
    
    # Kalo di grup tanpa reply
    elif message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply(
            f"**🆔 INFO GRUP**\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 Nama Grup: **{message.chat.title}**\n"
            f"🆔 Grup ID: `{message.chat.id}`\n"
            f"👥 Tipe: {message.chat.type}"
        )
    
    # Kalo di private chat
    else:
        reply_text = f"**🆔 INFO CHAT**\n"
        reply_text += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        reply_text += f"👤 Nama: **{message.chat.first_name}**"
        if message.chat.last_name:
            reply_text += f" {message.chat.last_name}"
        reply_text += f"\n"
        reply_text += f"🆔 User ID: `{message.chat.id}`\n"
        if message.chat.username:
            reply_text += f"👤 Username: @{message.chat.username}"
        await message.reply(reply_text)

@app.on_message(filters.command("whois", ".") & filters.me)
async def whois_command(client, message):
    """Lihat detail lengkap user"""
    
    # Tentukan target user
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            # Kalo pake username atau user id
            if message.command[1].startswith("@"):
                user = await client.get_users(message.command[1])
            else:
                user = await client.get_users(int(message.command[1]))
        except:
            await message.reply("❌ User tidak ditemukan!")
            return
    else:
        user = message.from_user
    
    status = await message.reply(f"🔄 **Mencari info {user.first_name}...**")
    
    try:
        # Ambil info lengkap
        full_user = await client.get_chat(user.id)
        
        # Ambil foto profil
        photos = []
        async for photo in client.get_chat_photos(user.id, limit=1):
            photos.append(photo)
        
        # Format teks
        teks = f"**📋 WHOIS: {user.first_name}**\n"
        teks += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        teks += f"👤 **Nama:** {user.first_name}"
        if user.last_name:
            teks += f" {user.last_name}"
        teks += f"\n"
        teks += f"🆔 **User ID:** `{user.id}`\n"
        
        if user.username:
            teks += f"🌐 **Username:** @{user.username}\n"
            teks += f"🔗 **Link:** t.me/{user.username}\n"
        else:
            teks += f"🌐 **Username:** Tidak ada\n"
        
        # Bio kalo ada
        if hasattr(full_user, 'bio') and full_user.bio:
            teks += f"📝 **Bio:** `{full_user.bio[:100]}`"
            if len(full_user.bio) > 100:
                teks += "..."
            teks += f"\n"
        
        # Status
        if hasattr(user, 'status'):
            status_text = str(user.status).replace("UserStatus.", "").capitalize()
            teks += f"📊 **Status:** {status_text}\n"
        
        # Foto profil
        teks += f"🖼️ **Foto profil:** {len(photos)} foto\n"
        
        # Data Center
        if hasattr(user, 'dc_id'):
            teks += f"📡 **DC ID:** {user.dc_id}\n"
        
        # Premium?
        if hasattr(user, 'is_premium') and user.is_premium:
            teks += f"⭐ **Premium:** Ya\n"
        
        # Bot?
        if hasattr(user, 'is_bot') and user.is_bot:
            teks += f"🤖 **Bot:** Ya\n"
        else:
            teks += f"👤 **Bot:** Bukan\n"
        
        teks += f"━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Kirim dengan foto kalo ada
        if photos:
            await message.reply_photo(
                photos[0].file_id,
                caption=teks
            )
            await status.delete()
        else:
            await status.edit(teks)
            
    except Exception as e:
        await status.edit(f"❌ Error: {str(e)}")

@app.on_message(filters.command("info", ".") & filters.me)
async def info_grup(client, message):
    """Info lengkap grup"""
    
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply("❌ Harus di dalam grup!")
        return
    
    status = await message.reply("🔄 **Mengambil info grup...**")
    
    try:
        full = await client.get_chat(message.chat.id)
        
        teks = f"**📊 INFO GRUP: {full.title}**\n"
        teks += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        teks += f"🆔 **ID Grup:** `{full.id}`\n"
        teks += f"👥 **Tipe:** {full.type}\n"
        
        if full.username:
            teks += f"🌐 **Username:** @{full.username}\n"
            teks += f"🔗 **Link:** t.me/{full.username}\n"
        
        if full.description:
            teks += f"📝 **Deskripsi:** `{full.description[:100]}`"
            if len(full.description) > 100:
                teks += "..."
            teks += f"\n"
        
        # Hitung anggota
        try:
            members_count = await client.get_chat_members_count(full.id)
            teks += f"👥 **Total anggota:** {members_count}\n"
        except:
            pass
        
        # Hitung admin
        try:
            admin_count = 0
            async for _ in client.get_chat_members(full.id, filter="administrators"):
                admin_count += 1
            teks += f"👑 **Admin:** {admin_count}\n"
        except:
            pass
        
        # Cek VC aktif
        if hasattr(full, 'is_voice_chat_started') and full.is_voice_chat_started:
            teks += f"🎤 **VC Aktif:** Ya\n"
        else:
            teks += f"🎤 **VC Aktif:** Tidak\n"
        
        # Cek restricted
        if hasattr(full, 'is_restricted') and full.is_restricted:
            teks += f"🔒 **Restricted:** Ya\n"
        
        # Cek scam
        if hasattr(full, 'is_scam') and full.is_scam:
            teks += f"⚠️ **Scam:** Ya\n"
        
        # Cek fake
        if hasattr(full, 'is_fake') and full.is_fake:
            teks += f"🎭 **Fake:** Ya\n"
        
        teks += f"━━━━━━━━━━━━━━━━━━━━━━━"
        
        # KIRIM FOTO DULU (kalo ada) BARU STATUS
        if full.photo:
            # Download dulu fotonya
            foto_path = await client.download_media(full.photo.big_file_id)
            
            # Kirim foto
            await client.send_photo(
                chat_id=message.chat.id,
                photo=foto_path,
                caption=teks
            )
            
            # Hapus file foto
            os.remove(foto_path)
            
            await status.delete()
        else:
            # Kalo gak ada foto, kirim teks aja
            await status.edit(teks)
            
    except Exception as e:
        await status.edit(f"❌ Error: {str(e)}")
