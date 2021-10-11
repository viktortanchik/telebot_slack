import os
import sqlite3
import time
from telethon import TelegramClient, sync, events
from telethon.tl.functions.channels import JoinChannelRequest

#================================Slack===================
import slack
from pathlib import Path
from dotenv import load_dotenv




flag =True
while(flag):
    db = sqlite3.connect('Account.db')
    cur = db.cursor()
    x = 1
    n = 0
    u = 0
    print("Очередь аккаунта № " + str(x))

    cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone)

    cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
    time.sleep(0.4)
    api_hash = str(cur.fetchone()[0])
    session = str("anon" + str(x))
    #client = TelegramClient(session, api_id, api_hash)
    flag=False
client = TelegramClient(session, api_id, api_hash)
client.connect()
time.sleep(2)

#channel_name = "https://t.me/zerno_agro_ua/85980"

#channel = 'ЗЕРНОВОЙ ЧАТ / АГРО🇺🇦'
#https://t.me/zerno_agro_ua/85980


channel_username = '@zerno_agro_ua'
client(JoinChannelRequest(channel_username))

################################################


@client.on(events.NewMessage)
async def my_event_handler(event):
    print(event.raw_text)# все новые сообщения
    sender_id = event.sender_id  # Получаем ID Юзера
    msg_id = event.id  # Получаем ID сообщения
    sender = await event.get_sender()
    if 'Glitch' in event.raw_text:
        #await event.reply('hi!')
        print(sender_id)
        print(sender.username)
        user =''.join(sender.username)
        userId=sender_id
        print(event.raw_text)
        mess=''.join(event.raw_text)
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        client_slack = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
        client_slack.chat_postMessage(channel='#test', text="user: "+str(user)+" userID: "+str(userId)+" Message: "+str(mess))

client.start()
client.run_until_disconnected()



