import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATA_FILE = "stats.json"


# ------------------ مدیریت آمار ------------------
def load_stats():
    if not os.path.exists(DATA_FILE):
        return {"start": 0, "buttons": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_stats(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# ------------------ لینک‌ها ------------------
LINKS = {
    "linkedin": ("👔 LinkedIn", "https://www.linkedin.com/in/alirezasoleimani-"),
    "stackoverflow": ("💻 Stack Overflow", "https://stackoverflow.com/users/23951445/alireza"),
    "github": ("🐙 GitHub", "https://github.com/Alireza-Soleimani-0"),
    "asnet": ("⚙️ AS Automation", "https://t.me/ASAutomation"),
    "anon": ("👤 Anonymous", "https://t.me/NoronChat_bot?start=sec-fhhchicadf"),
    "meas": ("📩 About Me", "https://t.me/+bimia6p-8dw0YTM0"),
}


# ------------------ استارت ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = load_stats()
    stats["start"] += 1
    save_stats(stats)

    keyboard = [
        [
            InlineKeyboardButton(LINKS["linkedin"][0], url=LINKS["linkedin"][1]),
            InlineKeyboardButton(LINKS["stackoverflow"][0], url=LINKS["stackoverflow"][1]),
        ],
        [
            InlineKeyboardButton(LINKS["github"][0], url=LINKS["github"][1]),
            InlineKeyboardButton(LINKS["asnet"][0], url=LINKS["asnet"][1]),
        ],
        [
            InlineKeyboardButton(LINKS["anon"][0], url=LINKS["anon"][1]),
            InlineKeyboardButton(LINKS["meas"][0], url=LINKS["meas"][1]),
        ],
        [
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
        ],
    ]

    await update.message.reply_text(
        "🔥 Welcome to Alireza Soleimani Bot\n\nChoose an option 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ------------------ دکمه Stats ------------------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "stats":
        stats = load_stats()

        text = "📊 Bot Stats\n\n"
        text += f"🚀 Total Starts: {stats['start']}\n\n"
        text += "🔘 Link Buttons:\n"

        for key in LINKS:
            count = stats["buttons"].get(key, 0)
            text += f"• {LINKS[key][0]} : {count}\n"

        await query.message.reply_text(text)


# ------------------ ثبت کلیک لینک ------------------
async def track_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.via_bot:
        return


# ------------------ اجرا ------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("🚀 Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
