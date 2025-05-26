# Schedule messages to be sent to group by bot 
# create the group in google sheet with the date and time 
# provide the group id and bot token

# Before running code,
# add the bot to the group
# run the following the command
# pip install pandas
# pip install python-telegram-bot

# proceed to run the code 'py scheduleMessage.py'

import pandas as pd
import requests
import time


while True:
    sheet_id = "1CXu8epOTKzdTO7VCDJNXK9htldiaTKyejviGMcACtCk"

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    df = pd.read_csv(url)
    df["Schedule Datetime"] = pd.to_datetime(df["Schedule Datetime"])

    previous_minute = pd.datetime.now() + pd.Timedelta(minutes=-1)
    print(type(previous_minute))

    current_time = pd.datetime.now()
    print(type(current_time))

    df = df[(df["Schedule Datetime"] > previous_minute) & (df["Schedule Datetime"] < current_time)]
    df

    def send_message(row):
        bot_id = "7690398188:AAFKtMXwastZZX5NZ1BW8PgkWJaMaSdJmTA"
        chat_id = "-4881983441"
        message = row[0]

        url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"

        return requests.get(url).json()

    if not df.empty:
        df['status'] = df.apply(send_message, axis = 1)
    time.sleep(60)
    df