from typing import Final
from dotenv import load_dotenv
import os


from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler

load_dotenv()
token = os.getenv("BOT_TOKEN")

TOKEN: Final = token
BOT_USERNAME: Final = "@shegz_demo_bot"


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hi! I'm your bot. How can Shegz help you today?")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! I'm your bot. Please type something so I can help!")



async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This is a custom command. You can add your own functionality here.")

# Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()
    """Process the input text and return a response."""

    if 'hello' in processed:
        return "Hello! How can I assist you today?"
    if 'how are you' in processed:
        return "I'm just a bot, but I'm here to help you!"
    if 'I love you' in processed:
        return "I appreciate your love! But I'm just a bot."
    
    return "I'm not sure how to respond to that. Can you ask me something else?"



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages from users."""
    message_type:str = update.message.chat.type
    
    text:str = update.message.text


    print(f'User ({update.message.chat.id}) in {message_type}: sent a message: {text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response:str = handle_response(new_text)
        else:
            return None
    
    else:
        response:str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to the user."""
    print(f'Update {update} caused error {context.error}')
    await update.message.reply_text('An error occurred. Please try again later.')



if __name__ == '__main__':
    print('Starting bot...')
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("custom", custom_command))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    application.add_error_handler(error_handler)

    # Run the bot until you send a signal to stop it
    print('Polling...')
    application.run_polling(poll_interval=3)