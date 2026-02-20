import os
import asyncio
import sqlite3
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
DB_PATH = "bot.db"

user_last_message = {}

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

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
        """
    )
    conn.commit()
    conn.close()

def add_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def get_users_count() -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    conn.close()
    return count

# ================= MENU =================
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

# ================= SAFE EDIT (FIXED) =================
async def safe_edit(query, text, markup):
    try:
        msg = query.message
        if msg and msg.photo:
            await query.edit_message_caption(
                caption=text,
                parse_mode="Markdown",
                reply_markup=markup,
            )
        else:
            await query.edit_message_text(
                text=text,
                parse_mode="Markdown",
                reply_markup=markup,
            )
    except Exception as e:
        print("Edit error:", e)

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)

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

    user_last_message[user_id] = msg

# ================= REPORT =================
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
    except Exception as e:
        print("Report error:", e)

def send_report(context, user, link_name):
    asyncio.create_task(send_report_async(context, user, link_name))

# ================= BUTTONS =================
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

    # 🔙 back
    if data == "back":
        await safe_edit(query, WELCOME_TEXT, main_menu())
        return

    # 📊 stats
    if data == "stats":
        stats_lines = [f"{k}: {v}" for k, v in click_stats.items()]
        stats_lines.append(f"users_started: {get_users_count()}")
        text = "\n".join(stats_lines)
        await safe_edit(query, f"📊 Stats\n\n{text}", back_button())
        return

    # 🔗 links
    if data in links:
        click_stats[data] += 1

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🚀 Open Link", url=links[data])],
                [InlineKeyboardButton("🔙 Back", callback_data="back")],
            ]
        )

        await safe_edit(query, "👇 Click the button below", keyboard)
        send_report(context, user, data)

# ================= RESET =================
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

# ================= MAIN =================
def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN not set")

    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    app.job_queue.run_repeating(reset_users, interval=3600, first=3600)

    print("🚀 Scalable Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
