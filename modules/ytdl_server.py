# --- LOGIKA DOWNLOAD (YT-DLP) ---
def sync_download(url, job_id, fmt="mp4"):
    try:
        # Template nama file
        out_template = os.path.join(DOWNLOAD_DIR, f"{job_id}-----%(title)s.%(ext)s")
        
        ydl_opts = {
            "outtmpl": out_template,
            "nocheckcertificate": True,
            "quiet": True,
        }

        # Logika khusus MP3
        if fmt == "mp3":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            })
        else:
            # Logika MP4 (Video)
            ydl_opts.update({
                "format": "bestvideo[height<=720]+bestaudio/best",
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Jika MP3, ganti ekstensi filename ke .mp3 karena hasil post-process
            if fmt == "mp3":
                filename = os.path.splitext(filename)[0] + ".mp3"
                
            progress_store[job_id] = {"status": "done", "file": filename}
            return filename
    except Exception as e:
        progress_store[job_id] = {"status": "error", "error": str(e)}
        return None

# --- COMMAND BARU UNTUK AUDIO (.yta) ---
@pyrogram_app.on_message(filters.command("yta", ".") & filters.me)
async def youtube_audio(client, message):
    if len(message.command) < 2:
        return await message.edit(error("Masukkan URL YouTube!"))

    url = message.command[1]
    job_id = str(uuid.uuid4())[:8]
    await message.edit(f"🎵 **Mengkonversi ke MP3...**\n`Job ID: {job_id}`")

    loop = asyncio.get_event_loop()
    file_path = await loop.run_in_executor(executor, sync_download, url, job_id, "mp3")

    if file_path and os.path.exists(file_path):
        await message.edit(f"📤 **Mengirim Audio...**")
        await client.send_audio(
            chat_id=message.chat.id,
            audio=file_path,
            caption=success(f"MP3 Berhasil diunduh!")
        )
        os.remove(file_path) # Hapus biar Termux gak penuh
        await message.delete()
    else:
        err = progress_store.get(job_id, {}).get("error", "Gagal konversi audio.")
        await message.edit(error(err))
