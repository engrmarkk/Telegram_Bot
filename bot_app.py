from typing import Final, Dict
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, Application
import os
from replies import start_response, pick_response
from dotenv import load_dotenv

load_dotenv()

TOKEN: Final = os.environ['BOT_TOKEN']
BOT_USERNAME: Final = os.environ['BOT_USERNAME']
LINK: Final = "https://www.teamflow.com"

# Dictionary to track user sessions
user_sessions: Dict[int, bool] = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    print(f'User {user_id} started the bot')
    user_sessions[user_id] = True  # Start a new session
    await update.message.reply_text(start_response())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'You can use the following commands:\n/start - Start the bot\n/help - Get help\n/custom - Custom command'
    )


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command response.')


def handle_response(text: str) -> str:
    text = text.upper().strip()
    return pick_response(text, LINK)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Check if the user is in an active session
    if user_sessions.get(user_id, False):
        if message_type == 'group' and BOT_USERNAME in text:
            text = text.replace(BOT_USERNAME, '').strip()

        response = handle_response(text)

        if text.upper().strip() == "D":
            user_sessions[user_id] = False  # End the session
            response = "Goodbye! To start a new conversation, type /start."

        await update.message.reply_text(response, parse_mode='HTML')
    else:
        # If not in a session, prompt the user to start a new session
        await update.message.reply_text("To start a conversation, type /start.")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Message handler for all text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    app.add_error_handler(error)

    # Polling
    print('Polling...')
    app.run_polling(poll_interval=5)
