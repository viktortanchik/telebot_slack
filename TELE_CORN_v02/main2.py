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


#user ='https://t.me/zerno_agro_ua' #ok
#user ='https://t.me/agroselhoz67'
#user = 'https://t.me/AgroTerritoriya'
x = 1
  # Получение одного сообщения


while True:
    # Список каналов
    USERS = ['https://t.me/zerno_agro_ua', 'https://t.me/agroselhoz67', 'https://t.me/AgroTerritoriya',
             'https://t.me/zerno_kombikorma', 'https://t.me/agro_trade',
             'https://t.me/evroexport', 'https://t.me/agrotsion', 'https://t.me/agromarketukr',
             'https://t.me/agro_bizUA', 'https://t.me/ukraineagro', 'https://t.me/worldagrotrade',
             'https://t.me/agrotender_zerno',
             'https://t.me/BusinessAGR', 'https://t.me/selhozztehnika', 'https://t.me/YUG_azoT',
             'https://t.me/avikon2020', 'https://t.me/udobreniya_ua', 'https://t.me/Ydobreniyaua',
             'https://t.me/AGO_GrainUa']

    for username in USERS:
        # Выбор канала
        # Авторизация пользователя
        db = sqlite3.connect('../Account.db')
        cur = db.cursor()
        cur.execute(f"SELECT PHONE FROM Account WHERE ID = '{x}'")
        time.sleep(0.4)
        Phone = str(cur.fetchone()[0])
        print("Входим в аккаунт: " + Phone, ' Номер ',x)
        cur.execute(f"SELECT API_ID FROM Account WHERE ID = '{x}'")
        time.sleep(0.4)
        api_id = str(cur.fetchone()[0])
        cur.execute(f"SELECT API_HASH FROM Account WHERE ID = '{x}'")
        time.sleep(0.4)
        api_hash = str(cur.fetchone()[0])
        session = str("anon" + str(x))

        client = TelegramClient(session, api_id, api_hash)
        client.start()
        x = x + 1
        # Выбор номера бота
        if x == 7:# Сброс счетчика номеров ботов
            x = 1
            print('Приостановка на 5 минут')
            time.sleep(300)

        print('работа с ' + username)
        dp = client.get_entity(username)
        messages = client.get_messages(dp, limit=100)#  Парсинг выбраного чата
        # Список ключевых слов
        lists = ['Продам зерно', 'Продам подсолнечник', 'Продам сою', ' Продам рапс',
                 'Продам лен', 'Продам Pапс', 'Продам пшеницу', 'Продам отходы семечки', 'Продам отходы сои',
                 'Продам отходы льна']

        for i in lists:# выбор определеного ключевого слова

            for message in messages:# выбор определеного Сообщения
                time.sleep(30)
                mess = []
                # sender = client.get_entity(message.sender_id)
                # print(message.sender_id, ':', sender.first_name, ':', message.text)

                mess.append(message.text)# Добавления сообщения в список
                print(mess)
                # print(i)
                # print(mess)
                temp_lists = ''.join(i)#  перевод списка в строку
                temp = ''.join(str(mess))  # " ".join(str(x) for x in mess) # ''.join(mess)
                # print(temp)
                ans = temp.find(temp_lists) # поиск в строке
                # print(ans)
                # temp = 0
                if ans > 0: #  если найдено совпадения
                    print('Ключевое слово ', i)
                    print('###############\n', temp)
                    print('#############\n ОТВЕТ \n', ans)
                    flag = False #  Флаг для необходим для проверки есть ли такая запис уже в файле
                    fp = open('example.csv', 'r', encoding='utf-8') #  чтения файла, в этот файл записевается сообщения
                    # которые уже были отправлиные
                    reader = csv.reader(fp, delimiter=';', lineterminator="\r")
                    for m in reader:#  чтения файла и поиск совподения по фойлу
                        print('Поиск по ФАЙЛУ')
                        cvs_m_temp = ''.join(m)#  перевод в строку
                        cvs_ans_temp = temp.find(cvs_m_temp) # Поиск
                        print('содержания Файла ', cvs_m_temp)
                        print('Текст сообщения ', temp)
                        # m = set(m)
                        # mess = set(mess)
                        # print(set(m) - set(mes[0]))
                        ##print(m)
                        # print(mess)

                        if cvs_ans_temp > 0:# Если совпадения найдено меняем флаг
                            # это позволит не отправлять сообщения которые мы уже отправляли
                            flag = True
                            print("Найдено совпадения !!!")
                            # fp.close()
                    fp.close()
                    if flag == False:  # Совпадений в файле не найдено
                        fp.close()
                        print("###########Запись и отправка ###########")
                        time.sleep(1)#  Отправка сообжения
                        client.send_message('@b_s_product', 'Поиск в чате ' + username)
                        time.sleep(1)
                        client.send_message('@b_s_product', 'Ключевое слово ' + i)
                        time.sleep(1)
                        client.forward_messages('@b_s_product', message)  # Пересылка сообщения
                        # print(message.sender_id, ':', sender.first_name, ':', message.text)
                        w_file = open("example.csv", mode="a", encoding='utf-8')# Запись в файл сообщения
                        file_writer = _csv.writer(w_file, delimiter=";", lineterminator="\r")
                        cvs_mes = []
                        cvs_mes.append(message.text)
                        file_writer.writerow(mess)
                        cvs_mes.clear()
                        mess.clear()
                        time.sleep(1)
                        w_file.close()
                else:
                    temp = 0
                    # print("Вот-же сука")
                    temp_lists = 0
                cvs_m_temp = 0
                temp_lists = 0
                cvs_ans_temp = 0
                mess.clear()

            temp = 0

            #x = x + 1
            #if x == 3:
                #x = 1





        # print(temp)
#USERS = ['https://t.me/zerno_agro_ua']
#lists= ['Продам отход','Продам зерно','отходы','Продам подсолнечник','Продам сою',' Продам рапс','Продам лен']
