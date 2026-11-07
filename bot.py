import os
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = [
    "@akhbarforyonline",
    "@trapstarmee"
]


async def check_membership(user_id, context):
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(
                chat_id=channel,
                user_id=user_id
            )

            if member.status not in ["member", "administrator", "creator"]:
                return False

        except Exception as e:
            print("Membership error:", e)
            return False

    return True


def join_keyboard():
    keyboard = [
        [InlineKeyboardButton(
            "📢 عضویت در کانال اول",
            url="https://t.me/akhbarforyonline"
        )],
        [InlineKeyboardButton(
            "📢 عضویت در کانال دوم",
            url="https://t.me/trapstarmee"
        )],
        [InlineKeyboardButton(
            "✅ عضو شدم",
            callback_data="check"
        )]
    ]

    return InlineKeyboardMarkup(keyboard)


def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🤖 چت هوشمند", callback_data="chat")],
        [InlineKeyboardButton("🎨 ساخت عکس", callback_data="image")],
        [InlineKeyboardButton("🌐 ترجمه", callback_data="translate")],
        [InlineKeyboardButton("ℹ️ درباره ما", callback_data="about")]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await check_membership(user_id, context):
        await update.message.reply_text(
            "🔒 برای استفاده از NOVA AI ابتدا عضو هر دو کانال شو:",
            reply_markup=join_keyboard()
        )
        return

    await update.message.reply_text(
        "✨ به NOVA AI خوش آمدی!\n\n"
        "دستیار هوشمند تو در تلگرام 🤖",
        reply_markup=main_keyboard()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if not await check_membership(user_id, context):
        await query.message.reply_text(
            "❌ هنوز عضو هر دو کانال نشدی!",
            reply_markup=join_keyboard()
        )
        return

    if query.data == "check":
        await query.message.reply_text(
            "✅ عضویت تأیید شد!\n\nبه NOVA AI خوش آمدی.",
            reply_markup=main_keyboard()
        )

    elif query.data == "chat":
        await query.message.reply_text("🤖 بخش چت هوشمند به زودی فعال می‌شود.")

    elif query.data == "image":
        await query.message.reply_text("🎨 بخش تولید تصویر به زودی فعال می‌شود.")

    elif query.data == "translate":
        await query.message.reply_text("🌐 بخش ترجمه به زودی فعال می‌شود.")

    elif query.data == "about":
        await query.message.reply_text("NOVA AI\nدستیار هوشمند تلگرام")


async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await check_membership(user_id, context):
        await update.message.reply_text(
            "🔒 ابتدا عضو کانال‌های ما شو:",
            reply_markup=join_keyboard()
        )
        return

    await update.message.reply_text(
        "🤖 موتور هوش مصنوعی هنوز متصل نشده است."
    )


async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN تنظیم نشده است")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

    print("NOVA AI Started!")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
