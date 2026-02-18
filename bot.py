import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# گرفتن توکن از Railway Variables
TOKEN = os.getenv("TOKEN")

keyboard = [
    ["🔗 LinkedIn"],
    ["💻 Stack Overflow"],
    ["🐙 GitHub"],
    ["🛡 ASnet Security"],
    ["📩 𝗔.𝗦 Anonymous"],
    ["📢 ME.AS"],  # دکمه جدید
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome to 𝗔𝗹𝗶𝗿𝗲𝘇𝗮 𝗦𝗼𝗹𝗲𝗶𝗺𝗮𝗻𝗶 Bot\n\nSelect an option:",
        reply_markup=reply_markup,
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔗 LinkedIn":
        await update.message.reply_text(
            "https://www.linkedin.com/in/alirezasoleimani-"
        )

    elif text == "💻 Stack Overflow":
        await update.message.reply_text(
            "https://stackoverflow.com/users/23951445/alireza"
        )

    elif text == "🐙 GitHub":
        await update.message.reply_text(
