# Helper Telegram Bot 🤖

A Telegram bot built using [Pyrogram](https://github.com/pyrogram/pyrogram) to manage users, handle join requests, and provide helpful commands for group/channel admins.

---

## 🚀 Features

- `/start` — Welcome message for users
- `/help` — List of available commands
- `/broadcast <message>` — Send a message to all users (admin only)
- `/stats` — Get total user count (admin only)
- `/users` — View first 10 registered users (admin only)
- `/kick <user_id>` — Remove user from database (admin only)
- MongoDB-based user database
- Cooldown handling to prevent command spamming

---

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/helper-telegram-bot.git
cd helper-telegram-bot
