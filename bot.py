import os
import json
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

# ================== تنظیمات ==================
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 5772782035  # ← آیدی عددی خودت

STATS_FILE = "stats.json"

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN is not set")

# ================== لینک‌ها ==================
LINKS = {
    "linkedin": "https://www.linkedin.com/in/alirezasoleimani-",
    "stackoverflow": "https://stackoverflow.com/users/23951445/alireza",
    "github": "https://github.com/Alireza-Soleimani-0",
    "asnet": "https://t.me/ASAutomation",
    "anonymous": "https://t.me/NoronChat_bot?start=sec-fhhchicadf",
    "about": "https://t.me/+bimia6p-8dw0YTM0",
}

# ================== مدیریت آمار ==================
def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"starts": 0, "buttons": {}}
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"starts": 0, "buttons": {}}


def save_stats(data):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def inc_start():
    data = load_stats()
    data["starts"] += 1
    save_stats(data)


def inc_button(name):
    data = load_stats()
    data["buttons"][name] = data["buttons"].get(name, 0) + 1
    save_stats(data)

# ================== کیبورد ==================
def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("👔 LinkedIn", callback_data="linkedin"),
            InlineKeyboardButton("💻 Stack Overflow", callback_data="stackoverflow"),
        ],
        [
            InlineKeyboardButton("🐙 GitHub", callback_data="github"),
            InlineKeyboardButton("⚙️ AS Automation", callback_data="asnet"),
        ],
        [
            InlineKeyboardButton("👤 Anonymous", callback_data="anonymous"),
            InlineKeyboardButton("📩 About Me", callback_data="about"),
        ],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ================== استارت ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inc_start()

    await update.message.reply_text(
        "🔥 Welcome to Alireza Soleimani Bot\n\nChoose an option 👇",
        reply_markup=get_keyboard()
    )

# ================== دکمه‌ها ==================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user = query.from_user

    # ---------- آمار ----------
    if data == "stats":
        stats = load_stats()

        text = "📊 Bot Stats\n\n"
        text += f"🚀 Total Starts: {stats['starts']}\n\n"
        text += "🔘 Button Clicks:\n"

        if stats["buttons"]:
            for k, v in stats["buttons"].items():
                text += f"• {k}: {v}\n"
        else:
            text += "No clicks yet"

        await query.message.reply_text(text)
        return

    # ---------- لینک‌ها ----------
    if data in LINKS:
        inc_button(data)

        # گزارش به ادمین
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"👆 {user.full_name} ({user.id}) clicked «{data}»"
            )
        except:
            pass

        await query.message.reply_text(
            f"🚀 Open Link:\n{LINKS[data]}"
        )

# ================== اجرا ==================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
