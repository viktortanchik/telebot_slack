import os
import sqlite3
import time
from telethon import TelegramClient, sync, events



db = sqlite3.connect('Account.db')
cur = db.cursor()

x = 1
flag =True
while(flag):
    n = 0
    u = 0
    print("Очередь аккаунта № " + str(x))
    if x == 23:
        x = x - 22
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
    client = TelegramClient(session, api_id, api_hash)
    client.start()
    flag =False


while True:
    @client.on(events.NewMessage(chats=('chat_name')))
    async def normal_handler(event):
        #    print(event.message)
        print(event.message.to_dict()['message'])