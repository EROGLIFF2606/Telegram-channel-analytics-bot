import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from settings import BOT_TOKEN
from bot_logic import start, set_channel, set_time, set_language, cancel, error_handler
from telegram import Update

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

CHOOSING, CHANNEL, TIME, LANGUAGE = range(4)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex("^(Set channel|Установить канал)$"), set_channel),
                MessageHandler(filters.Regex("^(Set time|Установить время)$"), set_time),
                MessageHandler(filters.Regex("^(Set language|Установить язык)$"), set_language),
            ],
            CHANNEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_channel)],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_time)],
            LANGUAGE: [MessageHandler(filters.Regex("^(English|Русский)$"), set_language)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()