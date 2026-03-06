# main.py
from app import app
import os
import importlib

# Load semua modules dari folder modules/
for file in os.listdir("modules"):
    if file.endswith(".py") and file != "__init__.py":
        module_name = file[:-3]
        importlib.import_module(f"modules.{module_name}")
        print(f"✅ Loaded module: {module_name}")

print("🔥 Userbot Started!")
app.run()
