# 🚀 Setup Guide - Fix API Key Error

## ❌ Error You're Seeing
```
AttributeError: The API key is required for new authorizations.
```

This error happens because required environment variables are missing.

---

## ✅ Step-by-Step Setup

### 1️⃣ Get Required Credentials

#### Get API_ID and API_HASH
1. Go to https://my.telegram.org/apps
2. Login with your Telegram account
3. Create a new application
4. Copy your **API_ID** and **API_HASH**

#### Get BOT_TOKEN
1. Open Telegram and search for **@BotFather**
2. Type `/newbot` and follow the instructions
3. Copy the **BOT_TOKEN** you receive

---

### 2️⃣ Create `.env` File

In your project root directory, create a `.env` file with at minimum:

```env
# REQUIRED - Get from https://my.telegram.org/apps
API_ID=your_api_id_here
API_HASH=your_api_hash_here

# REQUIRED - Get from @BotFather on Telegram
BOT_TOKEN=your_bot_token_here

# REQUIRED - Your Telegram ID (get from @userinfobot)
OWNER_ID=your_user_id_here

# REQUIRED - Create a private group and copy its ID (starts with -)
LOG_GROUP_ID=your_log_group_id_here

# Optional but recommended - MongoDB for database
MONGO_DB_URI=mongodb+srv://username:password@cluster.mongodb.net/database
```

---

### 3️⃣ Full `.env` Example

For a complete setup, copy `.env.example` and rename it to `.env`, then fill in your values:

```bash
cp .env.example .env
```

Then edit `.env` and replace all the `your_...` placeholders with actual values.

---

### 4️⃣ Verify Your Setup

Before running the bot, verify:
- ✅ `.env` file exists in the project root
- ✅ `BOT_TOKEN` is set
- ✅ `API_ID` is set
- ✅ `API_HASH` is set
- ✅ `OWNER_ID` is set
- ✅ `LOG_GROUP_ID` is set

---

### 5️⃣ Run the Bot

```bash
python -m VIPMUSIC
```

---

## 🆘 Still Getting Errors?

### `BOT_TOKEN is not set!`
- Open your `.env` file
- Make sure `BOT_TOKEN=` has a value (not empty)
- It should look like: `BOT_TOKEN=123456789:ABCDefGhIjKlMnOpQrStUvWxYz`

### `API_HASH is not set!`
- Open your `.env` file
- Make sure `API_HASH=` has a value
- Get it from https://my.telegram.org/apps

### `.env` file not being loaded
- Make sure `.env` is in the **project root** directory (same level as `VIPMUSIC` folder)
- Check that the filename is exactly `.env` (not `.env.txt` or `.env.example`)

### Database connection error
- If using MongoDB Atlas, make sure your IP is whitelisted in the Atlas console
- Check your `MONGO_DB_URI` connection string

---

## 📝 Important Notes

- **NEVER** commit `.env` to GitHub - it contains sensitive credentials
- The `.env.example` file is already in `.gitignore` 
- Keep your `BOT_TOKEN` and `API_HASH` secret
- If you accidentally leak credentials, regenerate them immediately

---

## 🔧 Need Help?

- [Pyrogram Documentation](https://docs.pyrogram.org/)
- [Telegram Bot API Docs](https://core.telegram.org/bots/api)
- [@BotFather](https://t.me/botfather) - For bot token help
