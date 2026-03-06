# modules/admin_tools.py
from app import app
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import ChatPermissions, ChatPrivileges
import os
from modules.styles import success, error, info, result_box

print("✅ Admin Tools loaded!")

@app.on_message(filters.command("ban", ".") & filters.me)
async def ban_user(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply(error("Harus di grup!"))
        return
    
    if not message.reply_to_message:
        await message.reply(error("Reply ke user yang mau di-ban!"))
        return
    
    user = message.reply_to_message.from_user
    
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply(success(f"{user.first_name} berhasil di-ban"))
    except Exception as e:
        await message.reply(error(f"Gagal: {str(e)}"))

@app.on_message(filters.command("kick", ".") & filters.me)
async def kick_user(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply(error("Harus di grup!"))
        return
    
    if not message.reply_to_message:
        await message.reply(error("Reply ke user yang mau di-kick!"))
        return
    
    user = message.reply_to_message.from_user
    
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.reply(success(f"{user.first_name} berhasil di-kick"))
    except Exception as e:
        await message.reply(error(f"Gagal: {str(e)}"))

@app.on_message(filters.command("unban", ".") & filters.me)
async def unban_user(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply(error("Harus di grup!"))
        return
    
    if len(message.command) < 2:
        await message.reply(error("Pake: .unban [user_id] atau reply ke pesan"))
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id = int(message.command[1])
        except:
            await message.reply(error("User ID gak valid"))
            return
    
    try:
        await client.unban_chat_member(message.chat.id, user_id)
        await message.reply(success(f"User {user_id} berhasil di-unban"))
    except Exception as e:
        await message.reply(error(f"Gagal: {str(e)}"))

@app.on_message(filters.command("mute", ".") & filters.me)
async def mute_user(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply(error("Harus di grup!"))
        return
    
    if not message.reply_to_message:
        await message.reply(error("Reply ke user yang mau di-mute!"))
        return
    
    user = message.reply_to_message.from_user
    
    try:
        await client.restrict_chat_member(
            message.chat.id, 
            user.id, 
            ChatPermissions(can_send_messages=False)
        )
        await message.reply(success(f"{user.first_name} berhasil di-mute"))
    except Exception as e:
        await message.reply(error(f"Gagal: {str(e)}"))

@app.on_message(filters.command("unmute", ".") & filters.me)
async def unmute_user(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply(error("Harus di grup!"))
        return
    
    if not message.reply_to_message:
        await message.reply(error("Reply ke user yang mau di-unmute!"))
        return
    
    user = message.reply_to_message.from_user
    
    try:
        await client.restrict_chat_member(
            message.chat.id, 
            user.id, 
            ChatPermissions(can_send_messages=True)
        )
        await message.reply(success(f"{user.first_name} berhasil di-unmute"))
    except Exception as e:
        await message.reply(error(f"Gagal: {str(e)}"))

@app.on_message(filters.command("del", ".") & filters.me)
async def delete_message(client, message):
    if not message.reply_to_message:
        await message.reply(error("Reply ke pesan yang mau dihapus!"))
        return
    
    try:
        await message.reply_to_message.delete()
        await message.delete()
    except Exception as e:
        await message.reply(error(f"Gagal: {str(e)}"))

@app.on_message(filters.command("purge", ".") & filters.me)
async def purge_messages(client, message):
    if not message.reply_to_message:
        await message.reply(error("Reply ke pesan pertama yang mau dihapus!"))
        return
    
    status = await message.reply("🔄 **Menghapus pesan...**")
    
    deleted = 0
    async for msg in client.get_chat_history(message.chat.id, limit=100):
        if msg.id >= message.reply_to_message.id:
            try:
                await msg.delete()
                deleted += 1
            except:
                pass
    
    await status.edit(result_box("PURGE", f"{deleted} pesan dihapus", "🧹"))

@app.on_message(filters.command("adminlist", ".") & filters.me)
async def admin_list(client, message):
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await message.reply(error("Harus di grup!"))
        return
    
    status = await message.reply("👑 **Mencari admin...**")
    
    try:
        admins = []
        async for member in client.get_chat_members(message.chat.id, filter="administrators"):
            if not member.user.is_bot:
                admins.append(member.user)
        
        if not admins:
            await status.edit("📭 **Admin:** Tidak ada admin")
            return
        
        text = ""
        for i, admin in enumerate(admins, 1):
            text += f"{i}. {admin.first_name}"
            if admin.last_name:
                text += f" {admin.last_name}"
            if admin.username:
                text += f" (@{admin.username})"
            text += "\n"
        
        await status.edit(result_box(f"ADMIN {message.chat.title}", text, "👑"))
    except Exception as e:
        await status.edit(error(f"Error: {str(e)}"))
