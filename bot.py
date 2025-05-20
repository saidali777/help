from pyrogram import Client, filters
from flask import Flask
import threading
import os

# Flask server for Koyeb health check
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

# Run Flask in a separate thread
def run_web():
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# Bot credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize Pyrogram bot
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🔥 Add this: A simple handler that replies to all private messages
@bot.on_message(filters.private & filters.text)
def reply(client, message):
    message.reply_text("Hello! I am alive and working on Koyeb 🚀")

bot.run()




