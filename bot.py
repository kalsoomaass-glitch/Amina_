from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import random
from flask import Flask
from threading import Thread

# ========= 24 HOUR ONLINE BOARD =========
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Amina Bot is 24/7 ONLINE 💖 - Replying to every message ✅"

def run_flask():
    app_flask.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()
# =======================================

TOKEN = "8875844712:AAGQFl56SwFEjpL_hN_pfvLgyfMOFisLdZw"
GROUP_LINK = "https://t.me/+DAQ4w6oJKfRiYjE0"
DEVELOPER_LINK = "https://t.me/Owner_official_pk"
CHANNEL_LINK = "https://t.me/pubgcardingtopups"

WELCOME_PHOTO = "amina_dp.jpg"
WELCOME_TEXT = """HEY 👋 I AM AMINA 💖

Your cute friend - I reply to every message 🥰
I am 24/7 ONLINE ✅
Make me admin, I will make group more lovely ✨

POWERED BY Rajput_ 👨‍💻"""

group_counter = {}

def get_reply(user_text, name):
    return random.choice([
        f"Heyy {name} 😍💖 I am ONLINE ✅ tell me 🥰",
        f"{name} jaan 😘💋 I am here 24/7 ONLINE 🌸 bolo? ✨",
        f"{name} baby 😚 I got your message 💖 I am active now 🔥",
        f"Aww {name} 😍 I reply to every message 💕 I am ONLINE ✅",
        f"{name} 😘 I am always online for you 💖 bolo kya baat hai? 🥰",
    ])

async def send_promo(update, context, is_private=False):
    keyboard = [
        [InlineKeyboardButton("ADD ME BABY 👶💋", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("DEVELOPER 🧑‍💻", url=DEVELOPER_LINK), InlineKeyboardButton("JOIN CHANNEL 📢", url=CHANNEL_LINK)],
        [InlineKeyboardButton("CHAT GROUP 🔥", url=GROUP_LINK)]
    ]
    caption = WELCOME_TEXT
    if is_private:
        caption += "\n\n💬 Owner se baat karni? 👉 @Owner_official_pk 🥰\nI am 24/7 ONLINE ✅"
    
    try:
        with open(WELCOME_PHOTO, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=caption, reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        await update.message.reply_photo(photo="https://i.imgur.com/8Km9tLL.jpg", caption=caption, reply_markup=InlineKeyboardMarkup(keyboard))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_promo(update, context, is_private=True)

async def inbox_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Inbox me har message pe reply + promo
    await send_promo(update, context, is_private=True)

async def group_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    chat_id = update.effective_chat.id
    group_counter[chat_id] = group_counter.get(chat_id, 0) + 1

    text = update.message.text or update.message.caption or "hi"
    name = update.message.from_user.first_name

    # Har message ka jawab - I am online
    reply = get_reply(text, name)
    await update.message.reply_text(reply)

    # Har 10 message ke baad promo with DP
    if group_counter[chat_id] % 10 == 0:
        await send_promo(update, context, is_private=False)

def main():
    keep_alive() # 24 hour online board start
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.ALL & ~filters.COMMAND, inbox_handler))
    app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.ALL & ~filters.COMMAND, group_handler))
    print("Bot is 24/7 ONLINE and replying to every message 💖")
    app.run_polling()

if __name__ == '__main__':
    main()