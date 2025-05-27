# Run this code for deployment on replit

from flask import Flask, render_template
from threading import Thread

app = Flask(automatedbot.py)

@app.route('/')
def index():
    return "Alive"

def run():
    app.run(host = '0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# This is a script to make bot auto respond to message and commands
# follow the following rules before running the script:
# 1 create the bot with bot father and get the bot token
# 2 turn group privacy on the bot settings
# 3 create the bot commands using one word on bot father
# 4  Before running code,
# 5 add the bot to the group
# 6 run the following the command
# 7 pip install pandas
# 7 pip install python-telegram-bot

# proceed to run the code 'py automatedBot.py'


import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re # Import re for regex filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Configuration ---
# Your Telegram Bot Token
TOKEN = "7697475103:AAF92b-oWCC6T3rKzd1f98erc0idEM6VFJc"

# Define the bot's commands and their descriptions
# This dictionary will be used to generate the command help message
BOT_COMMANDS = {
    "/start": "Begin interacting with BanesBot",
    "/name": "Find out BanesBot's name",
    "/owner": "Discover who owns BanesBot",
    "/bye": "Say goodbye to BanesBot",
    "/food": "Ask BanesBot about ordering food"
}

def get_commands_list_message():
    """Generates a formatted string of available commands."""
    commands_text = "Here are the commands I can respond to:\n\n"
    for cmd, desc in BOT_COMMANDS.items():
        commands_text += f"*{cmd}* - {desc}\n" # Use Markdown for bolding commands
    commands_text += "\nTry them out!"
    return commands_text

# --- Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command, greeting the user and listing all commands."""
    welcome_message = "Welcome on board!"
    commands_list = get_commands_list_message()
    await update.message.reply_text(f"{welcome_message}\n\n{commands_list}", parse_mode='Markdown')
    logger.info(f"Received /start from {update.effective_chat.id}. Listed commands.")

async def name_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /name command."""
    await update.message.reply_text(f"My name is BanesBot, happy to serve")
    logger.info(f"Received /name from {update.effective_chat.id}")

async def owner_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /owner command."""
    await update.message.reply_text(f"My owner is Bane")
    logger.info(f"Received /owner from {update.effective_chat.id}")

async def bye_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /bye command."""
    await update.message.reply_text("Do have a wonderful day!")
    logger.info(f"Received /bye from {update.effective_chat.id}")

async def food_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /food command."""
    await update.message.reply_text("Will you like me to order food for you at this moment?")
    logger.info(f"Received /food from {update.effective_chat.id}")

async def new_member_greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets new members when they join the group."""
    chat_id = update.effective_chat.id
    new_members = update.message.new_chat_members

    for member in new_members:
        # Check if the bot itself was added to avoid greeting itself
        if member.id == context.bot.id:
            # Bot was added to the group - greet and list command
            await context.bot.send_message(chat_id=chat_id,
                                          text="Thanks for adding me! I'm BanesBot, ready to help.\n\n" + get_commands_list_message(),
                                          parse_mode='Markdown')
            logger.info(f"Bot was added to group {chat_id}. Listed commands.")
        else:
            # A new user joined - greet them and suggest /start
            member_name = member.full_name
            await context.bot.send_message(chat_id=chat_id, text=f"Welcome, {member_name} to the group! Feel free to say hi or use /start to learn more about me.")
            logger.info(f"Greeted new member {member_name} in group {chat_id}")

async def generic_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles other general text messages not covered by specific commands.
    """
    chat_id = update.effective_chat.id
    message_text = update.message.text

    if update.effective_chat.type in ["group", "supergroup"]:
        logger.info(f"Received message in group {chat_id}: '{message_text}' from {update.effective_user.full_name}")
    else:
        logger.info(f"Received message from {chat_id}: '{message_text}'")

    # Respond to "hello" or "hi" by listing commands
    if message_text and ("hello" in message_text.lower() or "hi" in message_text.lower()):
        await update.message.reply_text(f"Hi there! I am BanesBot, how can I help you today?\n\n{get_commands_list_message()}", parse_mode='Markdown')
        logger.info(f"Bot replied to 'hello/hi' in {chat_id} with commands list.")

    # Your existing auto-response logic for guitars (if still desired)
    elif message_text and "guitar" in message_text.lower() and ("price" in message_text.lower() or "cost" in message_text.lower()):
        await update.message.reply_text("We have a wide range of guitars! Prices vary depending on the model. Could you tell me what type of guitar you're interested in?")
        logger.info(f"Bot replied to guitar query in {chat_id}")

    # General acknowledgement - be careful not to spam groups
    elif update.effective_chat.type in ["group", "supergroup"] and \
         message_text and \
         not message_text.startswith('/') and \
         not message_text.lower().startswith("bot"):
        pass # Keeping it silent for general messages by default


# --- Main Function to Run the Bot ---
def main() -> None:
    """Starts the bot."""
    application = Application.builder().token(TOKEN).build()

    # Register handlers for specific commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("name", name_command))
    application.add_handler(CommandHandler("owner", owner_command))
    application.add_handler(CommandHandler("bye", bye_command))
    application.add_handler(CommandHandler("food", food_command))

    # Register handler for new chat members
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member_greeting))

    # Register a generic handler for all other text messages that are not commands.
    # This should be added AFTER more specific CommandHandlers and StatusUpdate handlers.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generic_message_handler))

    logger.info("Bot started polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()