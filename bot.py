from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "YOUR_BOT_TOKEN"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔗 LinkedIn", url="https://linkedin.com")],
        [InlineKeyboardButton("💻 Stack Overflow", url="https://stackoverflow.com")],
        [InlineKeyboardButton("🐙 GitHub", url="https://github.com")],
        [InlineKeyboardButton("🛡 ASnet Security", url="https://t.me")],
        [InlineKeyboardButton("✉️ A.S Anonymous", url="https://t.me")],
        [InlineKeyboardButton("📢 ME.AS", url="https://t.me")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = (
        "🔥 *Welcome to Alireza Soleimani Bot*\n\n"
        "Select an option:"
    )

    await update.message.reply_photo(
        photo="https://i.imgur.com/your-banner.png",  # 🔥 بنر تو
        caption=caption,
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot is running...")
app.run_polling()
