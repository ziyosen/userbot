# modules/iptracker.py
from app import app
from pyrogram import filters
import requests
from modules.styles import success, error, info, result_box

print("✅ IP Tracker loaded!")

# ========== IP SEDERHANA ==========
@app.on_message(filters.command("ip", ".") & filters.me)
async def track_ip(client, message):
    if len(message.command) < 2:
        await message.reply(error("Pake: .ip [IP]\nContoh: .ip 8.8.8.8"))
        return
    
    ip = message.command[1]
    status = await message.reply("🔍 **Mencari IP...**")
    
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,org,as,proxy,hosting", timeout=10)
        data = r.json()
        
        if data.get("status") == "success":
            vpn = "YA" if data.get("proxy") or data.get("hosting") else "TIDAK"
            result = (
                f"📍 IP: {ip}\n"
                f"🌍 Negara: {data.get('country', 'N/A')}\n"
                f"🏙️ Kota: {data.get('city', 'N/A')}\n"
                f"📡 ISP: {data.get('isp', 'N/A')}\n"
                f"🔢 ASN: {data.get('as', 'N/A')}\n"
                f"🔒 VPN/Proxy: {vpn}"
            )
            await status.edit(result_box("HASIL IP", result, "🌐"))
        else:
            await status.edit(error("IP tidak valid"))
    except Exception as e:
        await status.edit(error(f"Error: {str(e)[:50]}"))

# ========== IP SAKTI ==========
@app.on_message(filters.command("ipsakti", ".") & filters.me)
async def ip_sakti(client, message):
    if len(message.command) < 2:
        await message.reply(error("Pake: .ipsakti [IP]\nContoh: .ipsakti 8.8.8.8"))
        return
    
    ip = message.command[1]
    status = await message.reply("🔍 **Menganalisis IP...**")
    
    try:
        # PAKE API YANG SAMA, TAPI LEBIH LENGKAP
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting", timeout=10)
        data = r.json()
        
        if data.get("status") == "success":
            vpn = "YA" if data.get("proxy") or data.get("hosting") else "TIDAK"
            mobile = "YA" if data.get("mobile") else "TIDAK"
            
            result = (
                f"📍 IP: {ip}\n"
                f"🌍 Negara: {data.get('country', 'N/A')}\n"
                f"🏙️ Kota: {data.get('city', 'N/A')}\n"
                f"🗺️ Region: {data.get('regionName', 'N/A')}\n"
                f"📮 Kodepos: {data.get('zip', 'N/A')}\n"
                f"🗺️ Koordinat: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}\n"
                f"📡 ISP: {data.get('isp', 'N/A')}\n"
                f"🏢 Organisasi: {data.get('org', 'N/A')}\n"
                f"🔢 ASN: {data.get('as', 'N/A')}\n"
                f"🕒 Timezone: {data.get('timezone', 'N/A')}\n"
                f"📱 Mobile: {mobile}\n"
                f"🔒 VPN/Proxy: {vpn}"
            )
            await status.edit(result_box("IP SUPER DETAIL", result, "🌐"))
        else:
            await status.edit(error("IP tidak valid"))
    except Exception as e:
        await status.edit(error(f"Error: {str(e)[:50]}"))

# ========== MY IP ==========
@app.on_message(filters.command("myip", ".") & filters.me)
async def my_ip(client, message):
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=10)
        ip = r.json().get("ip")
        await message.reply(result_box("IP PUBLIK", f"📍 {ip}", "🌐"))
    except:
        await message.reply(error("Gagal mendapatkan IP"))

# ========== SHERLOCK ==========
@app.on_message(filters.command("sherlock", ".") & filters.me)
async def sherlock_search(client, message):
    if len(message.command) < 2:
        await message.reply(error("Pake: .sherlock [username]"))
        return
    
    username = message.command[1]
    status = await message.reply("🔍 **Mencari username...**")
    
    sites = [
        {"name": "Instagram", "url": f"https://instagram.com/{username}"},
        {"name": "Twitter", "url": f"https://twitter.com/{username}"},
        {"name": "TikTok", "url": f"https://tiktok.com/@{username}"},
        {"name": "Facebook", "url": f"https://facebook.com/{username}"},
        {"name": "GitHub", "url": f"https://github.com/{username}"},
        {"name": "Reddit", "url": f"https://reddit.com/user/{username}"},
        {"name": "YouTube", "url": f"https://youtube.com/@{username}"},
    ]
    
    found = []
    for site in sites:
        try:
            r = requests.head(site["url"], timeout=5, allow_redirects=True)
            if r.status_code == 200:
                found.append(f"✅ {site['name']}: {site['url']}")
        except:
            pass
    
    if found:
        result = "\n".join(found[:10])
        await status.edit(result_box(f"HASIL UNTUK @{username}", result, "🔍"))
    else:
        await status.edit(error(f"Tidak ditemukan untuk @{username}"))

# ========== CEK NOMOR ==========
@app.on_message(filters.command("cekno", ".") & filters.me)
async def cek_nomor(client, message):
    if len(message.command) < 2:
        await message.reply(error("Pake: .cekno [nomor]\nContoh: .cekno 08123456789"))
        return
    
    nomor = message.command[1]
    nomor = nomor.replace(" ", "").replace("-", "").replace("+", "")
    
    if nomor.startswith("0"):
        nomor = "62" + nomor[1:]
    elif not nomor.startswith("62"):
        nomor = "62" + nomor
    
    provider = cek_provider(nomor)
    await message.reply(result_box("INFO NOMOR", f"📞 {nomor}\n📡 {provider}", "📱"))

def cek_provider(nomor):
    if nomor.startswith("62811") or nomor.startswith("62812") or nomor.startswith("62813") or nomor.startswith("62814") or nomor.startswith("62815"):
        return "Telkomsel (Halo/SimPATI)"
    elif nomor.startswith("62816") or nomor.startswith("62817") or nomor.startswith("62818") or nomor.startswith("62819"):
        return "Telkomsel (Kartu As)"
    elif nomor.startswith("62821") or nomor.startswith("62822") or nomor.startswith("62823"):
        return "XL"
    elif nomor.startswith("62831") or nomor.startswith("62832") or nomor.startswith("62833"):
        return "AXIS"
    elif nomor.startswith("62851") or nomor.startswith("62852") or nomor.startswith("62853"):
        return "Telkomsel (By.U)"
    elif nomor.startswith("62855") or nomor.startswith("62856") or nomor.startswith("62857") or nomor.startswith("62858"):
        return "Indosat (IM3)"
    elif nomor.startswith("62859"):
        return "Indosat (Mentari)"
    elif nomor.startswith("62877") or nomor.startswith("62878"):
        return "Tri (3)"
    elif nomor.startswith("62881") or nomor.startswith("62882") or nomor.startswith("62883") or nomor.startswith("62884") or nomor.startswith("62885") or nomor.startswith("62886") or nomor.startswith("62887") or nomor.startswith("62888") or nomor.startswith("62889"):
        return "Smartfren"
    else:
        return "Tidak diketahui"
