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

# آمار کلیک
click_stats = {
    "linkedin": 0,
    "stackoverflow": 0,
    "github": 0,
    "asnet": 0,
    "anon": 0,
    "meas": 0,
}

# ---------- منوی اصلی ----------
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🔷 LinkedIn Profile", url="https://www.linkedin.com/in/alirezasoleimani-")],
        [InlineKeyboardButton("🟠 Stack Overflow", url="https://stackoverflow.com/users/23951445/alireza")],
        [InlineKeyboardButton("⚫ GitHub Account", url="https://github.com/Alireza-Soleimani-0")],
        [InlineKeyboardButton("🛡 ASnet Security", url="https://t.me/ASnet01")],
        [InlineKeyboardButton("👤 A.S Anonymous", url="https://t.me/NoronChat_bot?start=sec-fhhchicadf")],
        [InlineKeyboardButton("📢 ME.AS Channel", url="https://t.me/+bimia6p-8dw0YTM0")],
        [InlineKeyboardButton("📊 View Stats", callback_data="stats")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo="https://i.imgur.com/8Km9tLL.jpg",  # اگر خواستی عوض کن
        caption=(
            "🔥 **Welcome to Alireza Soleimani Bot**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚀 Fast • Secure • Professional\n\n"
            "👇 Select an option below"
        ),
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )

# ---------- stats ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "stats":
        text = (
            "📊 **Bot Statistics**\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"LinkedIn clicks: {click_stats['linkedin']}\n"
            f"StackOverflow clicks: {click_stats['stackoverflow']}\n"
            f"GitHub clicks: {click_stats['github']}\n"
            f"ASnet clicks: {click_stats['asnet']}\n"
            f"Anonymous clicks: {click_stats['anon']}\n"
            f"ME.AS clicks: {click_stats['meas']}"
        )

        await query.message.reply_text(text, parse_mode="Markdown")

# ---------- main ----------
def main():
    if not TOKEN:
        raise ValueError("TOKEN is not set!")

    app = ApplicationBuilder().token(TOKEN).build
