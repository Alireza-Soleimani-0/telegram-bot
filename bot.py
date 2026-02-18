import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("TOKEN")

# ---------- کیبورد اینلاین ----------
def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("LinkedIn", url="https://www.linkedin.com/in/alirezasoleimani-")],
        [InlineKeyboardButton("Stack Overflow", url="https://stackoverflow.com/users/23951445/alireza")],
        [InlineKeyboardButton("GitHub", url="https://github.com/Alireza-Soleimani-0")],
        [InlineKeyboardButton("ASnet Security", url="https://t.me/ASnet01")],
        [InlineKeyboardButton("A.S Anonymous", url="https://t.me/NoronChat_bot?start=sec-fhhchicadf")],
        [InlineKeyboardButton("ME.AS", url="https://t.me/+bimia6p-8dw0YTM0")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- استارت ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo="https://i.imgur.com/8Km9tLL.jpg",  # اگر خواستی بنر خودت بزار
        caption=(
            "🔥 Welcome to 𝗔𝗹𝗶𝗿𝗲𝘇𝗮 𝗦𝗼𝗹𝗲𝗶𝗺𝗮𝗻𝗶 Bot\n\n"
            "Select an option:"
        ),
        reply_markup=main_keyboard(),
    )

# ---------- main ----------
def main():
    if not TOKEN:
        raise ValueError("TOKEN is not set!")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
