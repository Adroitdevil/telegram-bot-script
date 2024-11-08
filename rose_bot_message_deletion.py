import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler

# Set up logging to track bot activity and errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Define your bot token and admin user ID
TOKEN = "7556276586:AAGAW4ia7NyTPFOAiK_LymQDsiB6nnpfAto"
ROSE_BOT_ID = "MissRose_bot"
ADMIN_USER_ID = 6228577560

# Keywords to identify and delete specific messages from Rose Bot
DELETE_KEYWORDS = ["welcome", "rules", "joined", "chat", "verify", "group", "Go"]

# Function to delete messages after a delay of 10 seconds
async def delete_after_delay(message):
    try:
        await asyncio.sleep(10)  # Wait for 10 seconds
        await message.delete()  # Delete the message from the group
        logger.info(f"Message deleted successfully: {message.text}")  # Log success
    except Exception as e:
        logger.error(f"Error while deleting message: {e}")  # Log error if any occurs

# Handler to check and delete messages from Rose Bot
async def check_and_delete(update: Update, context):
    if update.message.from_user.username == ROSE_BOT_ID:  # Check if message is from Rose Bot
        message_text = update.message.text.lower()  # Get message text and make it lowercase

        # Check if the message contains any of the delete keywords
        if any(keyword.lower() in message_text for keyword in DELETE_KEYWORDS):
            logger.info(f"Message from Rose Bot detected: {message_text}")  # Log detected message
            await delete_after_delay(update.message)  # Delete after delay
        else:
            logger.info(f"Message from Rose Bot does not match keywords: {message_text}")  # Log non-matching message

# Command handler to allow the admin to control the bot
async def admin_commands(update: Update, context):
    if update.message.from_user.id == ADMIN_USER_ID:  # Check if user is the admin
        command = update.message.text.strip().lower()

        if command == "/startbot":
            logger.info("Bot started by admin.")  # Log bot activation
            await update.message.reply_text("Bot is now active and deleting messages.")
        elif command == "/stopbot":
            logger.info("Bot stopped by admin.")  # Log bot deactivation
            await update.message.reply_text("Bot is now inactive and will stop deleting messages.")
            # Additional code can be added here to stop the bot if needed
        else:
            await update.message.reply_text("Unknown command.")  # Handle unknown commands
    else:
        await update.message.reply_text("You are not authorized to control this bot.")  # Unauthorized access message

if __name__ == '__main__':
    # Initialize the application with the provided token
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers for processing messages and commands
    app.add_handler(MessageHandler(filters.TEXT, check_and_delete))  # Handle text messages from Rose Bot
    app.add_handler(CommandHandler("startbot", admin_commands))  # Handle /startbot command
    app.add_handler(CommandHandler("stopbot", admin_commands))  # Handle /stopbot command

    logger.info("Bot is running... Waiting for messages to delete.")  # Log bot status
    app.run_polling()
