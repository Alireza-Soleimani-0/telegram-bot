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

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS stats (
        key TEXT PRIMARY KEY,
        value INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
    """)

    conn.commit()
    conn.close()


def get_stat(key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM stats WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0


def inc_stat(key, amount=1):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO stats(key,value) VALUES(?,?) "
        "ON CONFLICT(key) DO UPDATE SET value=value+?",
        (key, amount, amount),
    )
    conn.commit()
    conn.close()


def add_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    conn.commit()
    conn.close()


def count_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    conn.close()
    return count


# ---------- TEXT ----------
WELCOME_TEXT = (
    "🔥 <b>Welcome to Alireza Soleimani Bot</b>\n\n"
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
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
    )


# ---------- SAFE EDIT ----------
async def safe_edit(query, text, markup):
    try:
        if query.message.photo:
            await query.edit_message_caption(
                caption=text,
                parse_mode="HTML",
                reply_markup=markup,
            )
        else:
            await query.edit_message_text(
                text=text,
                parse_mode="HTML",
                reply_markup=markup,
            )
    except Exception as e:
        print("Edit error:", e)


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    add_user(user_id)
    inc_stat("total_starts")

    try:
        with open(IMAGE_PATH, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=WELCOME_TEXT,
                parse_mode="HTML",
                reply_markup=main_menu(),
            )
    except:
        await update.message.reply_text(
            WELCOME_TEXT,
            parse_mode="HTML",
            reply_markup=main_menu(),
        )


# ---------- REPORT ----------
async def send_report_async(context, user, link_name):
    try:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = f"@{user.username}" if user.username else "ندارد"

        text = (
            f"📊 <b>New Click</b>\n\n"
            f"👤 Name: {user.full_name}\n"
            f"🆔 ID: <code>{user.id}</code>\n"
            f"🔗 Username: {username}\n"
            f"📍 Clicked: {link_name}\n"
            f"⏰ Time: {time}"
        )

        await context.bot.send_message(ADMIN_ID, text, parse_mode="HTML")
    except Exception as e:
        print("Report error:", e)


def send_report(context, user, link_name):
    asyncio.create_task(send_report_async(context, user, link_name))


# ---------- BUTTONS ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

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

    button_names = {
        "linkedin": "👔 LinkedIn",
        "stackoverflow": "💻 Stack Overflow",
        "github": "🐙 GitHub",
        "asnet": "⚙️ AS Automation",
        "anon": "👤 Anonymous",
        "meas": "📩 About Me",
    }

    valid = set(links.keys()) | {"back", "stats"}
    if data not in valid:
        await query.answer("نسخه قدیمی است، /start بزنید", show_alert=True)
        return

    # 🔙 back
    if data == "back":
        await safe_edit(query, WELCOME_TEXT, main_menu())
        return

    # 📊 stats (ادمین فقط)
    if data == "stats":
        if user.id != ADMIN_ID:
            await query.answer("⛔ Access denied", show_alert=True)
            return

        text = "📊 <b>Bot Stats</b>\n\n"
        text += f"👥 Users : <b>{count_users()}</b>\n"
        text += f"🚀 Total Starts : <b>{get_stat('total_starts')}</b>\n\n"

        for key in links.keys():
            text += f"• {key} : <b>{get_stat(key)}</b>\n"

        await safe_edit(query, text, back_button())
        return

    # ✅ ارسال لینک
    if data in links:
        inc_stat(data)

        await query.message.reply_text(
            f"{button_names[data]}\n🔗 {links[data]}"
        )

        send_report(context, user, data)


# ---------- MAIN ----------
def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN not set")

    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("🚀 Professional Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
