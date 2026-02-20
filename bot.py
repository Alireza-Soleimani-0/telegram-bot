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

click_stats = {
    "linkedin": 0,
    "stackoverflow": 0,
    "github": 0,
    "asnet": 0,
    "anon": 0,
    "meas": 0,
}

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
    try:
        with open(IMAGE_PATH, "rb") as photo:
            msg = await update.message.reply_photo(
                photo=photo,
                caption=WELCOME_TEXT,
                parse_mode="HTML",
                reply_markup=main_menu(),
            )
    except Exception as e:
        print("Photo error:", e)
        msg = await update.message.reply_text(
            WELCOME_TEXT,
            parse_mode="HTML",
            reply_markup=main_menu(),
        )

    user_last_message[update.effective_user.id] = msg


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

        await context.bot.send_message(
            ADMIN_ID, text, parse_mode="HTML"
        )
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

    # نام دکمه‌ها با ایموجی
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

    # 📊 stats
    if data == "stats":
        text = "📊 <b>Stats</b>\n\n"
        for k, v in click_stats.items():
            text += f"• {k} : <b>{v}</b>\n"

        await safe_edit(query, text, back_button())
        return

    # 🔗 links
    if data in links:
        click_stats[data] += 1

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(button_names[data], url=links[data])],
                [InlineKeyboardButton("🔙 Back", callback_data="back")],
            ]
        )

        await safe_edit(
            query,
            "👇 Click the button below",
            keyboard,
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
                parse_mode="HTML",
                reply_markup=main_menu(),
            )
        except:
            try:
                await msg.edit_text(
                    WELCOME_TEXT,
                    parse_mode="HTML",
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

    if app.job_queue:
        app.job_queue.run_repeating(reset_users, interval=3600, first=3600)

    print("🚀 Scalable Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
