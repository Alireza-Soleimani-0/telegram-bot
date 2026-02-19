import os
from datetime import datetime, timezone, timedelta
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
ADMIN_ID = 5772782035  # ← آیدی عددی خودت

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))

click_stats = {
    "linkedin": 0,
    "stackoverflow": 0,
    "github": 0,
    "asnet": 0,
    "anon": 0,
    "meas": 0,
}

WELCOME_TEXT = (
    "🔥 **Welcome to Alireza Soleimani Bot**\n\n"
    "Choose one of the options below 👇"
)

IMAGE_PATH = "bot.jpg"

# ---------- منوی اصلی ----------
def main_menu():
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
            InlineKeyboardButton("👤 Anonymous", callback_data="anon"),
            InlineKeyboardButton("📩 About Me", callback_data="meas"),
        ],
        [
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- دکمه بازگشت ----------
def back_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
    )

# ---------- ویرایش امن پیام ----------
async def safe_edit(query, text, markup):
    try:
        await query.edit_message_caption(
            caption=text,
            parse_mode="Markdown",
            reply_markup=markup,
        )
    except:
        await query.edit_message_text(
            text=text,
            parse_mode="Markdown",
            reply_markup=markup,
        )

# ---------- ثبت لاگ ----------
async def log_click(query, context, link_name):
    user = query.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "ندارد"
    fullname = f"{user.first_name or ''} {user.last_name or ''}".strip()
    time = datetime.now(IRAN_TZ).strftime("%Y-%m-%d %H:%M:%S")

    text = (
        f"📊 کلیک جدید ثبت شد\n\n"
        f"🔗 لینک: {link_name}\n"
        f"🕒 زمان: {time}\n"
        f"🆔 آیدی: `{user_id}`\n"
        f"👤 یوزرنیم: {username}\n"
        f"📛 نام: {fullname if fullname else 'ندارد'}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        parse_mode="Markdown"
    )

# ---------- start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(IMAGE_PATH, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=WELCOME_TEXT,
                parse_mode="Markdown",
                reply_markup=main_menu(),
            )
    except:
        await update.message.reply_text(
            WELCOME_TEXT,
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )

# ---------- مدیریت دکمه‌ها ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    links = {
        "linkedin": "https://www.linkedin.com/in/alirezasoleimani-",
        "stackoverflow": "https://stackoverflow.com/users/23951445/alireza",
        "github": "https://github.com/Alireza-Soleimani-0",
        "asnet": "https://t.me/ASAutomation",
        "anon": "https://t.me/NoronChat_bot",
        "meas": "https://t.me/+bimia6p-8dw0YTM0",
    }

    # بازگشت
    if data == "back":
        await safe_edit(query, WELCOME_TEXT, main_menu())
        return

    # آمار
    if data == "stats":
        text = (
            "📊 **Bot Statistics**\n\n"
            f"🔗 LinkedIn: {click_stats['linkedin']}\n"
            f"💻 StackOverflow: {click_stats['stackoverflow']}\n"
            f"🐙 GitHub: {click_stats['github']}\n"
            f"⚙️ ASnet: {click_stats['asnet']}\n"
            f"📩 Anonymous: {click_stats['anon']}\n"
            f"📢 About: {click_stats['meas']}"
        )
        await safe_edit(query, text, back_button())
        return

    # لینک‌ها
    if data in links:
        click_stats[data] += 1
        await log_click(query, context, data)

        text = f"🚀 **Open Link:**\n{links[data]}"
        await safe_edit(query, text, back_button())

# ---------- main ----------
def main():
    if not TOKEN:
        raise ValueError("TOKEN is not set!")

    print("🔥 Bot is running...")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

if __name__ == "__main__":
    main()
