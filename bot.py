import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

TOKEN = "YOUR_BOT_TOKEN"
PHOTO_URL = "https://i.imgur.com/your-image.jpg"  # عکس خودت

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# 🔥 کیبورد خفن با آیکون واقعی
def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "💼 LinkedIn",
                url="https://linkedin.com/in/yourusername"
            )
        ],
        [
            InlineKeyboardButton(
                "🧠 Stack Overflow",
                url="https://stackoverflow.com/users/yourid"
            )
        ],
        [
            InlineKeyboardButton(
                "🐙 GitHub",
                url="https://github.com/yourusername"
            )
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# 🚀 دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = (
        "🔥 Welcome to Alireza Soleimani Bot\n\n"
        "✨ Select an option below:"
    )

    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption=caption,
        reply_markup=get_keyboard()
    )

# ▶️ اجرا
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
