# bot.py

from pyrogram import Client
from flask import Flask
import threading
import os

# --- Flask web app to keep Koyeb happy ---
app = Flask(__name__)

@app.route("/")
def index():
    return "Pyrogram bot is running!"

def run_web():
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

# --- Start Flask in a background thread ---
threading.Thread(target=run_web).start()

# --- Start the Pyrogram bot ---
API_ID = int(os.getenv("API_ID", "your_api_id"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

bot.run()


