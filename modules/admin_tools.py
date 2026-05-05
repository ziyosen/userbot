import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message

# --- MODUL ADMIN GABUNGAN ---

@Client.on_message(filters.command(["adminlist"], prefixes=".") & filters.me)
async def adminlist_handler(client, message):
    if message.chat.type.value in ["private", "bot"]:
        return await message.edit("❌ Fitur ini hanya untuk Grup!")
    
    await message.edit("🔍 **Mengambil daftar admin...**")
    out_str = f"🛡️ **ADMIN LIST: {message.chat.title}**\n\n"
    owner = ""
    admins = []

    try:
        async for m in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            name = m.user.first_name if not m.user.is_deleted else "Akun Terhapus"
            if m.status == enums.ChatMemberStatus.OWNER:
                owner = f"👑 **Owner:** [{name}](tg://user?id={m.user.id})\n"
            else:
                admins.append(f"🔹 [{name}](tg://user?id={m.user.id})")
        
        full_list = owner + "\n".join(admins)
        await message.edit(full_list)
    except Exception as e:
        await message.edit(f"❌ **Gagal:** `{e}`")

@Client.on_message(filters.command(["ban", "kick", "unban"], prefixes=".") & filters.me)
async def member_mod_handler(client, message):
    cmd = message.command[0]
    if message.chat.type.value == "private":
        return await message.edit("❌ Gunakan di dalam grup!")

    # Cari User ID (dari reply atau input teks)
    user_id = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user_id = message.command[1]

    if not user_id:
        return await message.edit(f"❓ Mau di-{cmd} siapa? Reply ke orangnya atau ketik ID/Username.")

    try:
        if cmd == "ban":
            await client.ban_chat_member(message.chat.id, user_id)
            await message.edit(f"✅ User `{user_id}` berhasil di-**BAN**.")
        elif cmd == "kick":
            await client.ban_chat_member(message.chat.id, user_id)
            await client.unban_chat_member(message.chat.id, user_id)
            await message.edit(f"✅ User `{user_id}` berhasil di-**KICK**.")
        elif cmd == "unban":
            await client.unban_chat_member(message.chat.id, user_id)
            await message.edit(f"✅ User `{user_id}` sekarang bisa masuk lagi.")
    except Exception as e:
        await message.edit(f"❌ **Gagal:** Mungkin kamu bukan admin?\n`{e}`")

@Client.on_message(filters.command(["promote", "demote"], prefixes=".") & filters.me)
async def rank_handler(client, message):
    cmd = message.command[0]
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        return await message.edit("❌ Reply ke user untuk mengubah pangkat.")

    try:
        if cmd == "promote":
            await client.promote_chat_member(
                message.chat.id, 
                user_id,
                privileges=enums.ChatPrivileges(
                    can_manage_chat=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_promote_members=False,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                )
            )
            await message.edit("✅ Berhasil mempromosikan user jadi Admin!")
        elif cmd == "demote":
            await client.get_chat_member(message.chat.id, user_id)
            await client.promote_chat_member(
                message.chat.id, 
                user_id,
                privileges=enums.ChatPrivileges(
                    can_manage_chat=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_promote_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                )
            )
            await message.edit("✅ Jabatan Admin berhasil dicabut.")
    except Exception as e:
        await message.edit(f"❌ **Gagal:** `{e}`")

@Client.on_message(filters.command(["purge", "del"], prefixes=".") & filters.me)
async def delete_handler(client, message):
    if message.command[0] == "del":
        if message.reply_to_message:
            await message.reply_to_message.delete()
            await message.delete()
        else:
            await message.edit("❌ Reply ke pesan yang mau dihapus.")
    
    elif message.command[0] == "purge":
        if not message.reply_to_message:
            return await message.edit("❌ Reply ke pesan awal untuk memulai purge.")
        
        chat_id = message.chat.id
        message_ids = []
        
        # Ambil ID pesan dari yang di-reply sampai yang terbaru
        for i in range(message.reply_to_message.id, message.id):
            message_ids.append(i)
        
        # Hapus secara massal (Telegram limit per 100 pesan)
        await client.delete_messages(chat_id, message_ids)
        await message.edit(f"🧹 **{len(message_ids)} Pesan dibersihkan!**", delete_in=3)
        await asyncio.sleep(3)
        await message.delete()
