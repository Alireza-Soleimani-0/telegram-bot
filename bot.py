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

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATA_FILE = "stats.json"


# ------------------ فایل آمار ------------------
def load_stats():
    if not os.path.exists(DATA_FILE):
        return {"start": 0, "buttons": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_stats(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# ------------------ دکمه‌ها ------------------
BUTTONS = {
    "site": ("🌐 Website", "https://example.com"),
    "telegram": ("📢 Telegram", "https://t.me/example"),
    "instagram": ("📸 Instagram", "https://instagram.com/example"),
    "anonymous": ("👤 ناشناس", None),
}


# ------------------ استارت ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = load_stats()
    stats["start"] += 1
    save_stats(stats)

    keyboard = [
        [
            InlineKeyboardButton(
                BUTTONS["site"][0],
                callback_data="click_site",
            ),
            InlineKeyboardButton(
                BUTTONS["telegram"][0],
                callback_data="click_telegram",
            ),
        ],
        [
            InlineKeyboardButton(
                BUTTONS["instagram"][0],
                callback_data="click_instagram",
            ),
            InlineKeyboardButton(
                BUTTONS["anonymous"][0],
                callback_data="click_anonymous",
            ),
        ],
        [
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
        ],
    ]

    await update.message.reply_text(
        "یکی از گزینه‌ها را انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ------------------ هندل کلیک ------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    stats = load_stats()

    data = query.data

    # ---------- آمار ----------
    if data == "stats":
        text = "📊 آمار ربات:\n\n"
        text += f"🚀 تعداد استارت: {stats['start']}\n\n"

        text += "📌 کلیک دکمه‌ها:\n"
        for key in BUTTONS:
            count = stats["buttons"].get(key, 0)
            text += f"• {BUTTONS[key][0]} : {count}\n"

        await query.message.reply_text(text)
        return

    # ---------- کلیک دکمه ----------
    if data.startswith("click_"):
        key = data.replace("click_", "")

        # افزایش آمار
        stats["buttons"][key] = stats["buttons"].get(key, 0) + 1
        save_stats(stats)

        name, link = BUTTONS[key]

        # اگر لینک داشت → باز کن
        if link:
            await query.message.reply_text(
                f"🔗 {name}\n{link}"
            )
        else:
            await query.message.reply_text(
                "✉️ پیام ناشناس ارسال شد!"
            )


# ------------------ اجرا ------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
