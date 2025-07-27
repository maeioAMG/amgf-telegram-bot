import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from messages import MESSAGES, LANGUAGES

TOKEN = os.getenv("BOT_TOKEN")  # Pune aici tokenul tău de la BotFather sau folosește variabilă de mediu

SELECTING_LANGUAGE = 1

# Salvăm limba preferată a fiecărui user
user_lang = {}

def get_lang(update):
    uid = update.effective_user.id
    return user_lang.get(uid, "ro")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup([[LANGUAGES["ro"], LANGUAGES["en"]]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Alege limba / Choose your language:", reply_markup=reply_markup)
    return SELECTING_LANGUAGE

async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = "ro" if update.message.text == LANGUAGES["ro"] else "en"
    user_lang[update.effective_user.id] = lang
    await update.message.reply_text(MESSAGES[lang]["welcome"], reply_markup=None)
    return ConversationHandler.END

async def inscriere(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(MESSAGES[lang]["inscriere"])

async def despre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(MESSAGES[lang]["despre"])

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(MESSAGES[lang]["help"])

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_language)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("inscriere", inscriere))
    app.add_handler(CommandHandler("despre", despre))
    app.add_handler(CommandHandler("ajutor", help_cmd))
    app.add_handler(CommandHandler("help", help_cmd))

    print("Botul rulează...")  # Pentru debugging local
    app.run_polling()

if __name__ == "__main__":
    main()
