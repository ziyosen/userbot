import os
import uuid
import asyncio
import yt_dlp
from pyrogram import filters
from concurrent.futures import ThreadPoolExecutor
from app import app
from modules.styles import error, success

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
executor = ThreadPoolExecutor(max_workers=2)

def download_yt(url: str, format_type: str = "video") -> str | None:
    """Download YouTube video/audio. format_type: 'video' (360p) atau 'audio' (mp3)"""
    job_id = str(uuid.uuid4())
    out_template = os.path.join(DOWNLOAD_DIR, f"{job_id}%(title)s.%(ext)s")
    ydl_opts = {
        "outtmpl": out_template,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }
    if format_type == "audio":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:  # video 360p
        ydl_opts["format"] = "bestvideo[height<=360]+bestaudio/best / best[height<=360]"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_type == "audio":
                filename = os.path.splitext(filename)[0] + ".mp3"
            return filename
    except Exception as e:
        print(f"Download error: {e}")
        return None

@app.on_message(filters.command("yt", ".") & filters.me)
async def yt_video(client, message):
    if len(message.command) < 2:
        return await message.edit(error("Masukkan URL YouTube!"))
    url = message.command[1]
    status = await message.edit("📥 **Mendownload video (360p)...**")
    loop = asyncio.get_event_loop()
    file_path = await loop.run_in_executor(executor, download_yt, url, "video")
    if file_path and os.path.exists(file_path):
        await status.edit("📤 **Mengirim video...**")
        await client.send_video(message.chat.id, video=file_path, caption="🎬 Video dari YouTube")
        os.remove(file_path)
        await message.delete()
    else:
        await status.edit(error("Gagal download video. Coba link lain."))

@app.on_message(filters.command("yta", ".") & filters.me)
async def yt_audio(client, message):
    if len(message.command) < 2:
        return await message.edit(error("Masukkan URL YouTube!"))
    url = message.command[1]
    status = await message.edit("🎵 **Mendownload audio (MP3)...**")
    loop = asyncio.get_event_loop()
    file_path = await loop.run_in_executor(executor, download_yt, url, "audio")
    if file_path and os.path.exists(file_path):
        await status.edit("📤 **Mengirim audio...**")
        await client.send_audio(message.chat.id, audio=file_path, title="Audio dari YouTube")
        os.remove(file_path)
        await message.delete()
    else:
        await status.edit(error("Gagal download audio."))
