import sqlite3
import time
from telethon import TelegramClient
import csv
import _csv

from telethon.tl.functions.users import GetFullUserRequest

from telethon import sync, events
import re
import json

from telethon.tl.functions.contacts import ResolveUsernameRequest
# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetHistoryRequest


# для корректного переноса времени сообщений в json
from datetime import date, datetime
x = 1

db = sqlite3.connect('база/Account.db')
cur = db.cursor()
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


USERS = ['https://t.me/zerno_agro_ua','https://t.me/agroselhoz67','https://t.me/AgroTerritoriya']
#USERS = ['https://t.me/zerno_agro_ua']
lists= ['Продам отход','Продам зерно','отходы','Продам подсолнечник','Продам сою',' Продам рапс','Продам лен']
for username in USERS:
        print(username)
        #username = 'https://t.me/zerno_agro_ua' # канал @telegram
        # https://t.me/agroselhoz67
        # https://t.me/AgroTerritoriya
        #username = 'Electrowerty: заказы Дениса' # канал @telegram

        dp = client.get_entity(username)
        messages = client.get_messages(dp, limit=100) # Получение одного сообщения

        #participants = client.get_participants(username)
        '''
         Продам зерно
        поиск отходов  подсолнечник, соя, рапс (лен)
        '''
        mes=[]
        for message in messages:
                sender = client.get_entity(message.sender_id)
                #print(message.sender_id, ':', sender.first_name, ':', message.text)
                #,'Продам зерно','отходов','Продам отходы'

                for ls in lists:
                        #print(ls)
                        #print("ПОИС ПО ключивым Словам")
                        if ls in  message.text:
                                mes.append(message.text)

                                print("Ключевое слово Найдено ")
                                print(ls)
                                flag =False
                                #fp= open('example.csv', 'r', encoding='utf-8')
                                #reader = csv.reader(fp, delimiter=',', quotechar='"')
                                with open('example.csv') as f:
                                        reader = csv.reader(f)
                                for m in reader:
                                        print('Поиск по ФАЙЛУ')
                                        m=set(m)
                                        mes=set(mes)
                                        #print(set(m) - set(mes[0]))
                                        print(m)
                                        print(mes)

                                        if m == mes:
                                                flag =True
                                                print("Найдено совпадения !!!")
                                        mes.clear()


                                if flag ==False:# Совпадений в файле не найдено
                                        print("##############################")
                                        # client.forward_messages('@TessZhuma', message) # Пересылка сообщения
                                        print(message.sender_id, ':', sender.first_name, ':', message.text)
                                        #w_file = open("example.csv",mode="a", encoding='utf-8')
                                        #file_writer = _csv.writer(w_file, delimiter=",", lineterminator="\r")
                                        #file_writer.writerow(mes)
                                        with open('sw_data_new.csv', 'w') as f:
                                                writer = csv.writer(f)
                                        writer.writerow(message.text)

                                        mes.clear()
                                        time.sleep(1)

                                #w_file.close()





                                #Нужно сохронить сообщения для проверки на еденичность

