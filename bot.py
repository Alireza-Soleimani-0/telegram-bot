import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# توکن از Railway
TOKEN = os.getenv("BOT_TOKEN")

# آیدی عددی خودت
ADMIN_ID = 5772782035

IMAGE_PATH = "bot.jpg"

# ذخیره آخرین پیام کاربران برای ریست
user_last_message = {}

# آمار کلیک
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

# ---------- منو ----------
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
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
    )

# ---------- استارت ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(IMAGE_PATH, "rb") as photo:
            msg = await update.message.reply_photo(
                photo=photo,
                caption=WELCOME_TEXT,
                parse_mode="Markdown",
                reply_markup=main_menu(),
            )
    except:
        msg = await update.message.reply_text(
            WELCOME_TEXT,
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )

    user_last_message[update.effective_user.id] = msg

# ---------- ارسال گزارش ----------
async def send_report(context, user, link_name):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = f"@{user.username}" if user.username else "ندارد"

    text = (
        f"📊 **New Click**\n\n"
        f"👤 Name: {user.full_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"🔗 Username: {username}\n"
        f"📍 Clicked: {link_name}\n"
        f"⏰ Time: {time}"
    )

    await context.bot.send_message(ADMIN_ID, text, parse_mode="Markdown")

# ---------- دکمه‌ها ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    data = query.data

    links = {
        "linkedin": "https://www.linkedin.com/",
        "stackoverflow": "https://stackoverflow.com/",
        "github": "https://github.com/",
        "asnet": "https://t.me/",
        "anon": "https://t.me/",
        "meas": "https://t.me/",
    }

    if data == "back":
        await query.edit_message_caption(
            caption=WELCOME_TEXT,
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )
        return

    if data == "stats":
        text = "\n".join([f"{k}: {v}" for k, v in click_stats.items()])
        await query.edit_message_caption(
            caption=f"📊 Stats\n\n{text}",
            reply_markup=back_button(),
        )
        return

    if data in links:
        click_stats[data] += 1
        await send_report(context, user, data)

        await query.edit_message_caption(
            caption=f"🚀 **Open Link:**\n{links[data]}",
            parse_mode="Markdown",
            reply_markup=back_button(),
        )

# ---------- ریست ساعتی ----------
async def reset_users(context: ContextTypes.DEFAULT_TYPE):
    for user_id, msg in list(user_last_message.items()):

        # خودت ریست نشی
        if user_id == ADMIN_ID:
            continue

        try:
            await msg.edit_caption(
                caption=WELCOME_TEXT,
                parse_mode="Markdown",
                reply_markup=main_menu(),
            )
        except:
            try:
                await msg.edit_text(
                    WELCOME_TEXT,
                    parse_mode="Markdown",
                    reply_markup=main_menu(),
                )
            except:
                pass

# ---------- main ----------
def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN not set in Railway variables")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    # ریست هر ۱ ساعت
    app.job_queue.run_repeating(reset_users, interval=3600, first=3600)

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
