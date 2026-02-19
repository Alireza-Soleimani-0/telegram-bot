import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

# 👇 آیدی عددی خودت
ADMIN_ID = 123456789

# ذخیره زمان آخرین فعالیت هر کاربر
user_last_active = {}


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # ثبت زمان فعالیت
    user_last_active[user_id] = time.time()

    keyboard = [
        [InlineKeyboardButton("نمایش محتوا", callback_data="show")]
    ]

    await update.message.reply_text(
        "سلام 👋\nروی دکمه بزن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- BUTTON ----------------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    # ثبت زمان فعالیت
    user_last_active[user_id] = time.time()

    if query.data == "show":
        await query.message.edit_text("✅ این محتوای بات است")


# ---------------- RESET JOB ----------------
async def reset_users(context: ContextTypes.DEFAULT_TYPE):
    now = time.time()
    to_delete = []

    for user_id, last_time in user_last_active.items():
        # ادمین ریست نشه
        if user_id == ADMIN_ID:
            continue

        # اگر بیشتر از ۱ ساعت گذشته → پاک شود
        if now - last_time > 3600:
            to_delete.append(user_id)

    for uid in to_delete:
        del user_last_active[uid]

    if to_delete:
        print("Reset users:", to_delete)


# ---------------- MAIN ----------------
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    # اجرای ریست هر ۱ ساعت
    app.job_queue.run_repeating(reset_users, interval=3600, first=3600)

    print("Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
