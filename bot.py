import os
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 5772782035
IMAGE_PATH = "bot.jpg"

user_last_message = {}

# ✅ شمارنده استارت
start_count = 0

click_stats = {
    "linkedin": 0,
    "stackoverflow": 0,
    "github": 0,
    "asnet": 0,
    "anon": 0,
    "meas": 0,
}

# ✅ نام نمایشی دکمه‌ها
DISPLAY_NAMES = {
    "linkedin": "👔 LinkedIn",
    "stackoverflow": "💻 Stack Overflow",
    "github": "🐙 GitHub",
    "asnet": "⚙️ AS Automation",
    "anon": "👤 Anonymous",
    "meas": "📩 About Me",
}

WELCOME_TEXT = (
    "🔥 **Welcome to Alireza Soleimani Bot**\n\n"
    "Choose one of the options below 👇"
)

# ---------- MENU ----------
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
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back")]])

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global start_count
    start_count += 1  # ✅ افزایش شمارنده

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

# ---------- REPORT ----------
async def send_report_async(context, user, link_name):
    try:
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
    except:
        pass

def send_report(context, user, link_name):
    asyncio.create_task(send_report_async(context, user, link_name))

# ---------- BUTTONS ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
    except:
        return

    user = query.from_user
    data = query.data

    links = {
        "linkedin": "https://www.linkedin.com/in/alirezasoleimani-",
        "stackoverflow": "https://stackoverflow.com/users/23951445/alireza",
        "github": "https://github.com/Alireza-Soleimani-0",
        "asnet": "https://t.me/ASAutomation",
        "anon": "https://t.me/NoronChat_bot?start=sec-fhhchicadf",
        "meas": "https://t.me/+bimia6p-8dw0YTM0",
    }

    valid = set(links.keys()) | {"back", "stats"}
    if data not in valid:
        await query.answer("نسخه قدیمی است، /start بزنید", show_alert=True)
        return

    # ---------- BACK ----------
    if data == "back":
        try:
            await query.edit_message_caption(
                caption=WELCOME_TEXT,
                parse_mode="Markdown",
                reply_markup=main_menu(),
            )
        except:
            pass
        return

    # ---------- STATS ----------
    if data == "stats":
        stats_lines = "\n".join(
            [f"{DISPLAY_NAMES.get(k,k)} : {v}" for k, v in click_stats.items()]
        )

        caption = (
            "📊 **Bot Stats**\n\n"
            f"🚀 Starts : {start_count}\n\n"
            f"{stats_lines}"
        )

        await query.edit_message_caption(
            caption=caption,
            parse_mode="Markdown",
            reply_markup=back_button(),
        )
        return

    # ---------- LINKS ----------
    if data in links:
        click_stats[data] += 1

        # ✅ نمایش اسم لینک با ایموجی
        name = DISPLAY_NAMES.get(data, data)

        await query.edit_message_caption(
            caption=f"🚀 **{name}**\n{links[data]}",
            parse_mode="Markdown",
            reply_markup=back_button(),
        )

        send_report(context, user, data)

# ---------- RESET ----------
async def reset_users(context: ContextTypes.DEFAULT_TYPE):
    for uid, msg in list(user_last_message.items()):
        if uid == ADMIN_ID:
            continue
        try:
            await msg.edit_caption(
                caption=WELCOME_TEXT,
                parse_mode="Markdown",
                reply_markup=main_menu(),
            )
        except:
            pass

# ---------- MAIN ----------
def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN not set")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    app.job_queue.run_repeating(reset_users, interval=3600, first=3600)

    print("🚀 Scalable Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
