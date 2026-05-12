from app import app
from pyrogram import filters
import requests
import asyncio

print("✅ OSINT Module loaded!")

# ========== CEK IP SENDIRI ==========
@app.on_message(filters.command("myip", ".") & filters.me)
async def my_ip(client, message):
    try:
        r = requests.get("http://ip-api.com/json/", timeout=10).json()
        if r.get("status") == "fail":
            return await message.edit(f"❌ Gagal: {r.get('message')}")
        ip = r.get("query", "Tidak diketahui")
        await message.edit(f"🌐 **IP Publik Anda:** `{ip}`")
    except Exception as e:
        await message.edit(f"❌ Error: `{str(e)}`")

# ========== IP TRACKER ==========
@app.on_message(filters.command(["ip", "ipsakti"], ".") & filters.me)
async def track_ip(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Masukkan IP! Contoh: `.ipsakti 8.8.8.8`")
    
    ip = message.command[1]
    cmd = message.command[0]
    status = await message.edit(f"🔍 **Menganalisis IP {ip}...**")
    
    try:
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
        await status.edit(f"❌ **Error:** `{str(e)}`")

# ========== CEK NOMOR TELEPON (Indonesia) ==========
@app.on_message(filters.command("cekno", ".") & filters.me)
async def cek_nomor(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Contoh: `.cekno 0812xxxx`")
    
    raw = message.command[1].replace(" ", "").replace("-", "").replace("+", "")
    # Normalisasi
    if raw.startswith("0"):
        num = "62" + raw[1:]
    elif raw.startswith("62"):
        num = raw
    else:
        num = "62" + raw
    
    if len(num) < 10:
        return await message.edit("❌ Nomor terlalu pendek.")
    
    pref = num[:5]
    operator = "❓ Tidak diketahui"
    
    telkomsel = ["62811", "62812", "62813", "62821", "62822", "62823", "62851", "62852", "62853"]
    indosat   = ["62814", "62815", "62816", "62855", "62856", "62857", "62858"]
    xl_axis   = ["62817", "62818", "62819", "62831", "62838", "62859", "62877", "62878", "62879"]
    tri       = ["62895", "62896", "62897", "62898", "62899"]
    smartfren = ["62881", "62882", "62883", "62884", "62885", "62886", "62887", "62888", "62889"]
    
    if any(pref.startswith(x) for x in telkomsel):
        operator = "Telkomsel"
    elif any(pref.startswith(x) for x in indosat):
        operator = "Indosat Ooredoo"
    elif any(pref.startswith(x) for x in xl_axis):
        operator = "XL Axiata / Axis"
    elif any(pref.startswith(x) for x in tri):
        operator = "Tri (H3I)"
    elif any(pref.startswith(x) for x in smartfren):
        operator = "Smartfren"
    
    await message.edit(f"📱 **INFO NOMOR**\n━━━━━━━━━━━━━━━\n📞 **Nomor:** `{num}`\n📡 **Operator:** {operator}")

# ========== PENCARIAN SOSIAL MEDIA ==========
@app.on_message(filters.command("finduser", ".") & filters.me)
async def find_user(client, message):
    if len(message.command) < 2:
        return await message.edit("❌ Masukkan username! Contoh: `.finduser johndoe`")
    
    username = message.command[1].replace("@", "").strip()
    status_msg = await message.edit(f"🔍 **Mencari jejak @{username} di media sosial...**")
    await asyncio.sleep(1)
    
    sites = [
        f"🔗 [Instagram](https://instagram.com/{username})",
        f"🔗 [TikTok](https://tiktok.com/@{username})",
        f"🔗 [GitHub](https://github.com/{username})",
        f"🔗 [Twitter/X](https://x.com/{username})",
        f"🔗 [Facebook](https://facebook.com/{username})",
        f"🔗 [Telegram](https://t.me/{username})"
    ]
    await status_msg.edit(f"🛰️ **Hasil pencarian @{username}:**\n\n" + "\n".join(sites))
