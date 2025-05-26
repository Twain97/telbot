# This code runs and connect bot to chatgpt, this makes bot respond like human

# before proceed:

# run command: pip install python-telegram-bot openai
# get your bot token
# get your chatgpt api key

import telegram
from telegram.ext import Application, MessageHandler, CommandHandler, filters # Note the lowercase 'filters'
import openai
import os

# --- Configuration ---
# It's highly recommended to use environment variables for your API keys
TELEGRAM_BOT_TOKEN = "7697475103:AAF92b-oWCC6T3rKzd1f98erc0idEM6VFJc"
OPENAI_API_KEY = "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"

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# --- Telegram Bot Handlers ---

def start(update, context):
    """Sends a welcome message when the /start command is issued."""
    user_name = update.message.from_user.first_name
    update.message.reply_text(f"Hello {user_name}! 👋 I'm your ChatGPT-powered assistant. Send me a message, and I'll do my best to respond.")

def help_command(update, context):
    """Sends a help message when the /help command is issued."""
    update.message.reply_text("Simply send me any message, and I will forward it to ChatGPT to get a response. 🤖")

def handle_message(update, context):
    """Handles incoming text messages and gets a response from ChatGPT."""
    user_message = update.message.text
    chat_id = update.message.chat_id

    if not user_message:
        update.message.reply_text("Please send a text message. 🤔")
        return

    try:
        # Send the user's message to ChatGPT
        # You can customize the model and other parameters as needed
        # For newer OpenAI API versions (>=1.0.0), use the following:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        chatgpt_response = response.choices[0].message.content.strip()

        # For older OpenAI API versions (<1.0.0), use:
        # response = openai.Completion.create(
        # engine="text-davinci-003", # Or another suitable model
        # prompt=user_message,
        # max_tokens=150, # Adjust as needed
        # n=1,
        # stop=None,
        # temperature=0.7 # Adjust for creativity
        # )
        # chatgpt_response = response.choices[0].text.strip()


        # Send ChatGPT's response back to the user
        context.bot.send_message(chat_id=chat_id, text=chatgpt_response)

    except openai.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
        update.message.reply_text("Sorry, I encountered an error while contacting ChatGPT. Please try again later. 😥")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        update.message.reply_text("An unexpected error occurred. Please try again. 😵")

def main():
    """Starts the Telegram bot."""
    # Create the Application and pass it your bot's token.
    # It's good practice to use ApplicationBuilder for more complex setups
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build() # UPDATED INITIALIZATION

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non-command i.e message - forward to ChatGPT
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) # UPDATED FILTERS USAGE

    # Start the Bot
    print("Bot is starting... 🚀")
    # Run the bot until you press Ctrl-C
    application.run_polling() # UPDATED RUN METHOD

    print("Bot has stopped. 🛑")

if __name__ == '__main__':
    main()