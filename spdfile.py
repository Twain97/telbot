#this code lets user bot send a message to any group every 10 seconds(You can change the time as you want)

# Before running code,
# add the bot to the group
# run the following the command
# pip install pandas
# pip install python-telegram-bot

# proceed to run the code 'py spdfile.py'
import requests
import time
import pandas as pd # Import pandas for reading spreadsheets
from urllib.parse import quote_plus # Import quote_plus directly

while True:
    bot_id = "7690398188:AAFKtMXwastZZX5NZ1BW8PgkWJaMaSdJmTA"
    chat_id = "-1002565576111" # Updated chat_id as per your request
    # The Google Sheet ID has been updated to the new link you provided
    sheet_id = "1W3fvCTo8vfJdLwUTQf9bCK3rU3JH57vyuyWFRhYk1kU" 

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    
    try:
        # Read the CSV data from the Google Sheet URL into a pandas DataFrame
        df = pd.read_csv(url)
        
        # Check if the DataFrame is not empty
        if not df.empty:
            # Iterate through each row in the DataFrame
            # Assuming the message to send is in the first column (index 0) of the spreadsheet
            for index, row in df.iterrows():
                message_to_send = str(row.iloc[0]) # Extract the message from the first column

                # URL-encode the message to handle special characters like spaces, commas, etc.
                encoded_message = quote_plus(message_to_send)

                # Construct the Telegram API URL for sending the message
                telegram_url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={encoded_message}"
                
                # Send the HTTP GET request to the Telegram API
                response = requests.get(telegram_url).json()
                
                # Check the response from Telegram
                if response.get("ok"):
                    print(f"Message sent: '{message_to_send}'. Response: {response}")
                else:
                    print(f"Failed to send message: '{message_to_send}'. Error: {response.get('description', 'Unknown error')}")
        else:
            print("Spreadsheet is empty or no messages found to send.")

    except requests.exceptions.RequestException as e:
        print(f"Network error while trying to fetch spreadsheet or send message: {e}")
    except pd.errors.EmptyDataError:
        print("Spreadsheet is empty or contains no data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Wait for 5 seconds before the next iteration
    time.sleep(10)
