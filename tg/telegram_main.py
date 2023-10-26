import logging
import os
import parser

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

__all__ = ['telegram_start']

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def __start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hello, this is Test Application for Epic Games News")
    for game_element in parser.EpicParser().parse():
        await update.message.reply_text(
            f"Title: {game_element.get_title()}\n"
            f"Description: {game_element.get_description()}\n"
            f"Original price: {game_element.get_original_price()}\n"
            f"Image: {game_element.get_img()}\n"
            f"From: {game_element.get_from_date()}\n"
            f"To: {game_element.get_to_date()}\n"
        )


async def __help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def __echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def telegram_start() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    load_dotenv('.env')

    application = Application.builder().token(os.getenv('token')).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", __start))
    application.add_handler(CommandHandler("help", __help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, __echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)