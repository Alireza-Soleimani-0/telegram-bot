import os
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

# ------------------ آمار کلیک ------------------
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

# ------------------ منوی اصلی (دو ستونه) ------------------
def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🔗 LinkedIn", callback_data="linkedin"),
            InlineKeyboardButton("💻 Stack Overflow", callback_data="stackoverflow"),
        ],
        [
            InlineKeyboardButton("🐙 GitHub", callback_data="github"),
            InlineKeyboardButton("🛡 𝔸.𝕊 𝙿𝙻𝙲|𝙰𝚞𝚝𝚘𝚖𝚊𝚝𝚒𝚘𝚗 ", callback_data="asnet"),
        ],
        [
            InlineKeyboardButton("📩 A.S Anonymous", callback_data="anon"),
            InlineKeyboardButton("📢about ME", callback_data="meas"),
        ],
        [
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# ------------------ دکمه بازگشت ------------------
def back_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back", callback_data="back")]]
    )

# ------------------ start ------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(IMAGE_PATH, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=WELCOME_TEXT,
                parse_mode="Markdown",
                reply_markup=main_menu(),
            )
    except FileNotFoundError:
        await update.message.reply_text(
            WELCOME_TEXT,
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )

# ------------------ مدیریت دکمه‌ها ------------------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    links = {
        "linkedin": "https://www.linkedin.com/in/alirezasoleimani-",
        "stackoverflow": "https://stackoverflow.com/users/23951445/alireza",
        "github": "https://github.com/Alireza-Soleimani-0",
        "asnet": "https://t.me/ASAutomation",
        "anon": "https://t.me/NoronChat_bot?start=sec-fhhchicadf",
        "meas": "https://t.me/+bimia6p-8dw0YTM0",
    }

    # ---------- بازگشت ----------
    if data == "back":
        try:
            with open(IMAGE_PATH, "rb") as photo:
                await query.message.reply_photo(
                    photo=photo,
                    caption=WELCOME_TEXT,
                    parse_mode="Markdown",
                    reply_markup=main_menu(),
                )
        except FileNotFoundError:
            await query.edit_message_caption(
                caption=WELCOME_TEXT,
                parse_mode="Markdown",
                reply_markup=main_menu(),
            )
        return

    # ---------- آمار ----------
    if data == "stats":
        text = (
            "📊 **Bot Statistics**\n\n"
            f"🔗 LinkedIn: {click_stats['linkedin']}\n"
            f"💻 StackOverflow: {click_stats['stackoverflow']}\n"
            f"🐙 GitHub: {click_stats['github']}\n"
            f"🛡 ASnet: {click_stats['asnet']}\n"
            f"📩 Anonymous: {click_stats['anon']}\n"
            f"📢 about ME.AS: {click_stats['meas']}"
        )

        await query.edit_message_caption(
            caption=text,
            parse_mode="Markdown",
            reply_markup=back_button(),
        )
        return

    # ---------- لینک‌ها ----------
    if data in links:
        click_stats[data] += 1

        await query.edit_message_caption(
            caption=f"🚀 **Open Link:**\n{links[data]}",
            parse_mode="Markdown",
            reply_markup=back_button(),
        )

# ------------------ main ------------------
def main():
    if not TOKEN:
        raise ValueError("TOKEN is not set!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("🔥 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
