"""
Бот для поиска ключевых слов в новых сообщениях ( в личке и групах ), и перессылке сообщения в Slack.

"""
#================================telethon===================
import os
import sqlite3
import time
from telethon import TelegramClient, sync, events
from telethon.tl.functions.channels import JoinChannelRequest
#================================Slack===================
import slack
from pathlib import Path
from dotenv import load_dotenv


class Bot:

    def __init__(self, accounts=1):
        #self.client = client
        self.accounts = accounts

    def create_db(self,phone,Api_id,Api_hash): # Функция для регистрации, принемает номер телефона,Api_id, Api_hash
        db = sqlite3.connect('Account.db')
        cur = db.cursor()
        # Создаем таблицу
        cur.execute("""CREATE TABLE IF NOT EXISTS Account (
            ID INTEGER PRIMARY KEY,
            PHONE TEXT,
            PASS TEXT,
            API_ID TEXT,
            API_HASH TEXT,
            ACTIVITY TEXT
        )""")
        db.commit()
        #phone = phone #"+380661054982"
        password = "13236546460"
        #Api_id = "1634158"
        #Api_hash = "1ea650a5f73b4074a90f8e2a086d2641"
        Activity = "ON"
        cur.execute(f"SELECT PHONE FROM Account WHERE PHONE = '{phone}'")
        if cur.fetchone() is None:
            cur.execute("""INSERT INTO Account(PHONE, PASS, API_ID, API_HASH, ACTIVITY) VALUES (?,?,?,?,?);""",
                        (phone, password, Api_id, Api_hash, Activity))
            db.commit()
            print("Зарегистрированно!")
            for value in cur.execute("SELECT * FROM Account"):
                print(value)

    def create_clients(self,X):# Функция для создания сесии, принемает количество новеров в базе.
        db = sqlite3.connect('Account.db')
        cur = db.cursor()
        x = 1
        while (True):
            print("Очередь аккаунта № " + str(x))
            cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
            time.sleep(0.2)
            Phone = str(cur.fetchone()[0])
            print("Входим в аккаунт: " + Phone)
            cur.execute(f"SELECT PASS FROM Account WHERE ID = '{x}'")
            time.sleep(0.2)
            password = str(cur.fetchone()[0])
            print(password)
            cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
            time.sleep(0.2)
            api_id = str(cur.fetchone()[0])
            cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
            time.sleep(0.2)
            api_hash = str(cur.fetchone()[0])
            session = str("anon" + str(x))
            client = TelegramClient(session, api_id, api_hash)
            client.start()
            x = x + 1
            time.sleep(1)
            if x == X:
                print("Aккаунты активированы!")
                break

    def account_start(self):# Функция старта клиента
        db = sqlite3.connect('Account.db')
        cur = db.cursor()
        x = self.accounts
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
        self.client = TelegramClient(session, api_id, api_hash)
        self.client.connect()
        time.sleep(2)

    def join_chat(self, channel_username): # Функция для присойденения к группам. Пример названия группы'@zerno_agro_ua'
        client = self.client
        client(JoinChannelRequest(channel_username))

    def main_bot(self,text):# Функция для поиска в новых сообщениях ключевых слов и переадресации в Slack
        client = self.client
        @client.on(events.NewMessage)
        async def my_event_handler(event):
            print(event.raw_text)  # все новые сообщения
            sender_id = event.sender_id  # Получаем ID Юзера
            msg_id = event.id  # Получаем ID сообщения
            sender = await event.get_sender()
            for i in text:
                if i in event.raw_text:
                    # await event.reply('hi!')
                    print(sender_id)
                    print(sender.username)
                    user = ''.join(sender.username)
                    userId = sender_id
                    print(event.raw_text)
                    mess = ''.join(event.raw_text)
                    env_path = Path('.') / '.env' #  Токен для бота SLACK_API_TOKEN
                    load_dotenv(dotenv_path=env_path)
                    client_slack = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
                    client_slack.chat_postMessage(channel='#test', text="user: " + str(user) + " userID: " + str(
                        userId) + " Message: " + str(mess))
        self.client.start()
        self.client.run_until_disconnected()

start = Bot(1)
start.account_start()
texts=['test','text','yes']
start.main_bot(texts)

