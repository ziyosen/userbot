# app.py
from pyrogram import Client
from config import API_ID, API_HASH

app = Client(
    "myuserbot",
    api_id=API_ID,
    api_hash=API_HASH,
    workers=20
)
