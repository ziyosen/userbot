from app import app
from pyrogram import filters
import requests
import asyncio

print("✅ IP Tracker & OSINT loaded!")

# --- LOGIKA IP TRACKER (Sederhana & Sakti digabung) ---
@app.on_message(filters.command(["ip", "ipsakti"], ".") & filters.me)
async def track_ip(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Masukkan IP! Contoh: `.ipsakti 8.8.8.8`")
    
    ip = message.command[1]
    cmd = message.command[0]
    status = await message.edit(f"🔍 **Menganalisis IP {ip}...**")
    
    try:
        # Field diperlengkap untuk ipsakti
        fields = "status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting"
        r = requests.get(f"http://ip-api.com/json/{ip}?fields={fields}", timeout=10).json()
        
        if r.get("status") == "fail":
            return await status.edit(f"❌ **Gagal:** `{r.get('message')}`")

        vpn = "YA" if r.get("proxy") or r.get("hosting") else "TIDAK"
        
        res = (
            f"🌐 **IP INFO:** `{ip}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 **Lokasi:** {r.get('city')}, {r.get('regionName')}, {r.get('country')}\n"
            f"📮 **Kodepos:** `{r.get('zip')}`\n"
            f"📡 **ISP/Org:** {r.get('isp')} / {r.get('org')}\n"
            f"🔒 **VPN/Hosting:** `{vpn}`\n"
        )
        
        if cmd == "ipsakti":
            res += (
                f"📱 **Mobile Net:** `{r.get('mobile')}`\n"
                f"🕒 **Timezone:** {r.get('timezone')}\n"
                f"📍 **Koordinat:** `{r.get('lat')}, {r.get('lon')}`\n"
                f"🔗 **Maps:** [Klik Disini](https://www.google.com/maps?q={r.get('lat')},{r.get('lon')})"
            )
        
        await status.edit(res, disable_web_page_preview=True)
    except Exception as e:
        await status.edit(f"❌ **Error:** `{str(e)[:50]}`")

# --- LOGIKA CEK NOMOR (Prefix Perbaikan) ---
@app.on_message(filters.command("cekno", ".") & filters.me)
async def cek_nomor(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Contoh: `.cekno 0812xxx`")
    
    num = message.command[1].replace(" ", "").replace("-", "")
    if num.startswith("0"): num = "62" + num[1:]
    if not num.startswith("62"): num = "62" + num
    
    # Perbaikan Logika Prefix Operator Indonesia
    pref = num[:5] # Ambil 5 digit depan (628xx)
    operator = "Tidak Diketahui"
    
    tsel = ["62811", "62812", "62813", "62821", "62822", "62851", "62852", "62853"]
    isat = ["62815", "62816", "62855", "62856", "62857", "62858"]
    xl_ax = ["62817", "62818", "62819", "62859", "62877", "62878", "62831", "62838"]
    tri = ["62895", "62896", "62897", "62898", "62899"]
    sfren = ["62881", "62882", "62883", "62884", "62885", "62886", "62887", "62888", "62889"]

    if any(pref.startswith(x) for x in tsel): operator = "Telkomsel"
    elif any(pref.startswith(x) for x in isat): operator = "Indosat Ooredoo"
    elif any(pref.startswith(x) for x in xl_ax): operator = "XL Axiata / Axis"
    elif any(pref.startswith(x) for x in tri): operator = "Tri (H3I)"
    elif any(pref.startswith(x) for x in sfren): operator = "Smartfren"

    await message.edit(f"📱 **INFO NOMOR**\n━━━━━━━━━━━━━━━\n📞 **Nomor:** `{num}`\n📡 **Operator:** {operator}")

# --- LOGIKA SOSMED SEARCH (Biar gak bingung, ganti nama ke .finduser) ---
@app.on_message(filters.command("finduser", ".") & filters.me)
async def find_user(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Masukkan username!")
    
    user = message.command[1].replace("@", "")
    await message.edit(f"🔍 **Mencari jejak @{user} di Sosmed...**\n(Ini bukan lacak lokasi GPS!)")
    
    sites = [
        f"🔗 [Instagram](https://instagram.com/{user})",
        f"🔗 [TikTok](https://tiktok.com/@{user})",
        f"🔗 [GitHub](https://github.com/{user})",
        f"🔗 [Twitter/X](https://x.com/{user})"
    ]
    await asyncio.sleep(1.5)
    await message.edit(f"🛰️ **Hasil pencarian @{user}:**\n\n" + "\n".join(sites))
