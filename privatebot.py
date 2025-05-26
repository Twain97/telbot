#this code lets user bots send message to any group every 10 seconds(You can change the time as you want)

# Before running code,
# add the bot to the group
# run the following the command
# pip install pandas
# pip install python-telegram-bot

# proceed to run the code 'py privatebot.py'
import requests
import time
from urllib.parse import quote_plus # Import quote_plus directly

while True:
    bot_id = "7690398188:AAFKtMXwastZZX5NZ1BW8PgkWJaMaSdJmTA"
    chat_id = "-1002565576111"
    
    # Define the message to send
    message_to_send = "Hello, this is a test bot created to send message to group every 5 seconds"

    # URL-encode the message to handle special characters
    encoded_message = quote_plus(message_to_send)

    url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={encoded_message}"
    
    try:
        response = requests.get(url).json()
        if response.get("ok"):
            print(f"Message sent: '{message_to_send}'. Response: {response}")
        else:
            print(f"Failed to send message: '{message_to_send}'. Error: {response.get('description', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"Network error sending message: '{message_to_send}'. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while sending message: '{message_to_send}'. Error: {e}")

    # Wait for 30 seconds before the next iteration
    time.sleep(5)
