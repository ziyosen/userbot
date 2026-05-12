from app import app
from pyrogram import filters
import random

# Daftar pesan absen
absen_list = [
    "**Hadir dong Benxx** 😁",
    "**Hadir Kaka Ganteng** 😉",
    "**Gua Hadir, Ada Apa?** 😎",
    "**Gua Hadir Ganteng** 🥵",
    "**Hadir Ngab, Lagi di Genteng** 😂",
    "**Hadir Bang, Lagi Mandiin Lele** 🐟",
    "**Si Cakep Hadir Bang** 😎",
    "**Hadir, tapi lagi berak** 💩",
    "**Benxx hadir! Jangan sibuk-sibuk amat** 🥱",
]

# Daftar pujian "aku ganteng"
ganteng_list = [
    "**Iya Ganteng Banget** 😍",
    "**Gantengnya Gak Ada Lawan** 😚",
    "**Kamu Gantengnya Aku Kan** 😍",
    "**Iyaa, gak ada saingan** 😎",
    "**Lu emang ganteng, tapi boong** 😏",
    "**Ganteng sih, tapi aku lebih** 🥴",
    "**Bener, lu cakep bet dah** ✨",
]

@app.on_message(filters.command("absen", ".") & filters.me)
async def absen_cmd(client, message):
    """Balas dengan pesan hadir random."""
    await message.edit(random.choice(absen_list))

@app.on_message(filters.command("aku_ganteng", ".") & filters.me)
async def aku_ganteng_cmd(client, message):
    """Balas dengan pujian diri random."""
    await message.edit(random.choice(ganteng_list))
