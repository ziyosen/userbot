# 🔥 Akeo Userbot

Userbot Telegram pribadi dengan fitur lengkap untuk manajemen grup, broadcast, OSINT, dan admin tools.

## ✨ Fitur

**📦 CORE**: .ping .alive .uptime  
**🚫 BLACKLIST**: .bl .unbl .listbl .gcast  
**👑 ADMIN**: .ban .kick .unban .mute .unmute .del .purge .settitle .setphoto .adminlist .promote .demote  
**🛠️ TOOLS**: .stiker .emoji .id .whois .info  
**🔍 OSINT**: .ip .ipsakti .myip .sherlock .cekno  
**📊 SYSTEM**: .stats .sysinfo .botinfo  

## 🚀 Install di Termux
```bash
pkg update && pkg upgrade
pkg install python git
pip install pyrogram psutil requests pillow
git clone https://github.com/akeorunyrd-ai/AkeoUserbot.git
cd AkeoUserbot
cp config.example.py config.py
nano config.py  # Isi API_ID & API_HASH
python main.py
