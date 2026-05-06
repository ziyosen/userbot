from app import app
import os
import importlib

print("🚀 Memulai Benxx Userbot...")

# Pastikan folder modules ada
if not os.path.exists("modules"):
    os.makedirs("modules")

# Load semua modules dari folder modules/
for file in os.listdir("modules"):
    if file.endswith(".py") and file != "__init__.py":
        module_name = file[:-3]
        try:
            importlib.import_module(f"modules.{module_name}")
            print(f"✅ Loaded: {module_name}")
        except Exception as e:
            # Jika ada satu modul rusak, yang lain tetap jalan
            print(f"❌ Failed to load {module_name}: {e}")

print("🔥 Userbot is Online!")
app.run()
