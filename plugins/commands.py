import time
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS
from .database import add_user, get_all_users, users_collection

user_cooldowns = {}

def cooldown(seconds=10):
    def decorator(func):
        async def wrapper(client, message, *args, **kwargs):
            user_id = message.from_user.id
            now = time.time()
            last_called = user_cooldowns.get(user_id, 0)
            if now - last_called < seconds:
                await message.reply(f"Please wait {int(seconds - (now - last_called))} seconds before using this command again.")
                return
            user_cooldowns[user_id] = now
            await func(client, message, *args, **kwargs)
        return wrapper
    return decorator

@Client.on_message(filters.command("start"))
async def start(client, message):
    await add_user(message.from_user.id, message.from_user.username or "")
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Support Group", url="https://t.me/colonel_support")],
            [InlineKeyboardButton("Updates", url="https://t.me/colonol_updates")]
        ]
    )
    await message.reply(
        f"Hello {message.from_user.mention}! 👋\nI am your helper bot.\nUse /help to see commands.",
        reply_markup=keyboard
    )

@Client.on_message(filters.command("help"))
async def help(client, message):
    text = """
Available commands:
/start - Start the bot
/help - This help message
/broadcast <text> - (Admin only) Broadcast message to all users
/stats - (Admin only) Show total users
/users - (Admin only) List first 10 users
/kick <user_id> - (Admin only) Remove user from database
"""
    await message.reply(text)

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
@cooldown(20)
async def broadcast(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /broadcast <message>")
    text = message.text.split(None, 1)[1]

    users = await get_all_users()
    count = 0
    for user in users:
        try:
            await client.send_message(user["_id"], text)
            count += 1
        except Exception:
            pass

    await message.reply(f"Broadcast sent to {count} users.")

@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats(client, message):
    count = await users_collection.count_documents({})
    await message.reply(f"Total users: {count}")

@Client.on_message(filters.command("users") & filters.user(ADMINS))
async def users_list(client, message):
    cursor = users_collection.find({}).limit(10)
    users = [f"- {user['_id']} (@{user.get('username', 'N/A')})" async for user in cursor]
    await message.reply("Users:\n" + "\n".join(users) if users else "No users found.")

@Client.on_message(filters.command("kick") & filters.user(ADMINS))
async def kick(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /kick <user_id>")
    user_id = int(message.command[1])
    result = await users_collection.delete_one({"_id": user_id})
    if result.deleted_count:
        await message.reply(f"User {user_id} removed from database.")
    else:
        await message.reply(f"User {user_id} not found.")

