# modules/clone.py
from app import app
from pyrogram import filters, enums
from pyrogram.types import Message
import os
import json
from datetime import datetime

print("✅ Clone module loaded!")

DATA_FILE = "data/clone_backup.json"
os.makedirs("data", exist_ok=True)

def load_backup():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_backup(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Blacklist username/ID yang tidak boleh di-clone (developer)
BLACKLIST_USERNAMES = ["Benxx", "bleszh"]  # ganti dengan username developer
BLACKLIST_IDS = []  # bisa tambah ID numerik

def is_blacklisted(user) -> bool:
    if user.id in BLACKLIST_IDS:
        return True
    if user.username and user.username.lower() in [x.lower() for x in BLACKLIST_USERNAMES]:
        return True
    return False

async def get_full_user(client, user_id):
    """Mendapatkan UserFull (nama, bio, foto) dari user ID/username."""
    try:
        user = await client.get_users(user_id)
        full = await client.get_chat(user.id)
        bio = full.bio if hasattr(full, 'bio') else ""
        # Ambil photo ID jika ada
        photos = await client.get_profile_photos(user.id, limit=1)
        photo_file_id = photos[0].file_id if photos else None
        return user, bio, photo_file_id
    except Exception as e:
        return None, None, None

@app.on_message(filters.command("clone", ".") & filters.me)
async def clone_cmd(client, message: Message):
    args = message.text.split(maxsplit=1)
    input_args = args[1] if len(args) > 1 else ""

    # Restore
    if input_args == "restore":
        backup = load_backup()
        me = await client.get_me()
        if str(me.id) not in backup:
            return await message.edit("❌ Kamu belum pernah clone siapa pun. Tidak ada data untuk restore.")

        old = backup[str(me.id)]
        await message.edit("🔄 Mengembalikan identitas asli...")
        try:
            # Update nama
            await client.update_profile(
                first_name=old.get("first_name", ""),
                last_name=old.get("last_name", "")
            )
            # Update bio
            if old.get("bio"):
                await client.update_profile(bio=old["bio"])
            # Update foto jika ada
            if old.get("photo_file_id"):
                await client.set_profile_photo(photo=old["photo_file_id"])
            # Hapus backup
            del backup[str(me.id)]
            save_backup(backup)
            await message.edit("✅ Identitas asli berhasil dikembalikan!")
        except Exception as e:
            await message.edit(f"❌ Gagal restore: `{e}`")
        return

    # Clone target
    target_user = None
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    elif input_args:
        try:
            target_user = await client.get_users(input_args)
        except:
            return await message.edit("❌ User tidak ditemukan.")
    else:
        return await message.edit("❌ Gunakan: `.clone @username/id` atau reply ke user, atau `.clone restore`")

    # Cek blacklist (developer)
    if is_blacklisted(target_user):
        return await message.edit("❌ **Tidak dapat mengkloning akun developer Benxx!**")

    # Simpan data asli userbot (pertama kali)
    me = await client.get_me()
    backup = load_backup()
    if str(me.id) not in backup:
        # Backup data asli
        my_photos = await client.get_profile_photos(me.id, limit=1)
        my_photo_file_id = my_photos[0].file_id if my_photos else None
        my_full = await client.get_chat(me.id)
        my_bio = my_full.bio if hasattr(my_full, 'bio') else ""
        backup[str(me.id)] = {
            "first_name": me.first_name,
            "last_name": me.last_name or "",
            "bio": my_bio,
            "photo_file_id": my_photo_file_id
        }
        save_backup(backup)

    await message.edit(f"🎭 Mengganti identitas menjadi `{target_user.first_name}`...")

    # Ambil data target
    target, target_bio, target_photo_file_id = await get_full_user(client, target_user.id)
    if not target:
        return await message.edit("❌ Gagal mendapatkan data target.")

    # Update profil
    try:
        await client.update_profile(
            first_name=target.first_name,
            last_name=target.last_name or ""
        )
        if target_bio:
            await client.update_profile(bio=target_bio)
        if target_photo_file_id:
            # Hapus foto lama? Pyrogram akan mengganti otomatis
            await client.set_profile_photo(photo=target_photo_file_id)
        await message.edit(f"✅ Berhasil mengkloning {target.first_name}!\nGunakan `.clone restore` untuk kembali.")
    except Exception as e:
        await message.edit(f"❌ Gagal clone: `{e}`")
