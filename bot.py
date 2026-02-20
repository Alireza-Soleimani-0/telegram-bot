import os
import asyncio
import sqlite3
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.error import Forbidden, BadRequest

# ================== CONFIG ==================
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 5772782035
IMAGE_PATH = "bot.jpg"
DB_PATH = "bot.db"

# ================== FAST DATABASE ==================
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            key TEXT PRIMARY KEY,
            value INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()

def get_stat(key: str) -> int:
    cursor.execute("SELECT value FROM stats WHERE key=?", (key,))
    row = cursor.fetchone()
    return row[0] if row else 0

def inc_stat(key: str, amount: int = 1):
    cursor.execute(
        "INSERT INTO stats(key,value) VALUES(?,?) "
        "ON CONFLICT(key) DO UPDATE SET value=value+?",
        (key, amount, amount),
    )
    conn.commit()

def add_user(user_id: int):
    cursor.execute(
        "INSERT OR IGNORE INTO users(user_id) VALUES(?)",
        (user_id,),
    )
    conn.commit()

def get_all_users():
    cursor.execute("SELECT user_id FROM users")
    return [row[0] for row in cursor.fetchall()]

def count_users() -> int:
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]

# ================== TEXT ==================
WELCOME_TEXT = (
    "🔥 <b>Welcome to Alireza Soleimani Bot</b>\n\n"
    "Choose one of the options below 👇"
)

# ================== MENU ==================
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

# ================== SAFE EDIT ==================
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
    except Exception:
        pass

# ================== START ==================
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

# ================== ADMIN REPORT (ASYNC TURBO) ==================
async def send_report(context, user, link_name):
    try:
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = f"@{user.username}" if user.username else "ندارد"

        text = (
            f"📊 <b>New Click</b>\n\n"
            f"👤 {user.full_name}\n"
            f"🆔 <code>{user.id}</code>\n"
            f"🔗 {username}\n"
            f"📍 {link_name}\n"
            f"⏰ {time_now}"
        )

        await context.bot.send_message(ADMIN_ID, text, parse_mode="HTML")
    except:
        pass

# ================== BUTTONS ==================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(cache_time=60)  # ⚡ پاسخ فوری

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

    if data == "back":
        await safe_edit(query, WELCOME_TEXT, main_menu())
        return

    if data == "stats":
        if user.id != ADMIN_ID:
            await query.answer("⛔ Access denied", show_alert=True)
            return

        text = (
            "📊 <b>Bot Stats</b>\n\n"
            f"👥 Users : <b>{count_users()}</b>\n"
            f"🚀 Total Starts : <b>{get_stat('total_starts')}</b>\n"
        )
        await safe_edit(query, text, back_button())
        return

    if data in links:
        inc_stat(data)

        await query.message.reply_text(
            f"{button_names[data]}\n🔗 {links[data]}",
            disable_web_page_preview=True,
        )

        asyncio.create_task(send_report(context, user, data))

# ================== 🚀 TURBO BROADCAST ==================
async def sms_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.from_user.id != ADMIN_ID:
        return

    if not msg.reply_to_message:
        await msg.reply_text("❌ روی پیام ریپلای کن بعد sms بفرست")
        return

    status = await msg.reply_text("🚀 Turbo SMS started...")

    users = get_all_users()
    total = len(users)

    success = 0
    failed = 0
    blocked = 0

    sem = asyncio.Semaphore(30)  # ⚡ سرعت بالا

    async def send_one(uid):
        nonlocal success, failed, blocked
        async with sem:
            try:
                await context.bot.copy_message(
                    chat_id=uid,
                    from_chat_id=msg.chat_id,
                    message_id=msg.reply_to_message.message_id,
                )
                success += 1
            except Forbidden:
                blocked += 1
                failed += 1
            except BadRequest:
                failed += 1
            except Exception:
                failed += 1

    tasks = [asyncio.create_task(send_one(u)) for u in users]
    await asyncio.gather(*tasks)

    await status.edit_text(
        f"✅ SMS Finished\n\n"
        f"👥 Total: {total}\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}\n"
        f"🚫 Blocked: {blocked}"
    )

# ================== MAIN ==================
def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN not set")

    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex(r"(?i)^sms$"), sms_broadcast)
    )

    print("🚀 TURBO BOT RUNNING...")
    app.run_polling()

if __name__ == "__main__":
    main()
