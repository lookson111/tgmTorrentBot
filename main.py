"""
    Написано Иматдиновым Ринатом
    работает на python 3.7.9
"""

import telebot
import config
import bottoken
import os
import time
import sys
import threading
import configparser
import psutil
from qbittorrent import Client
import pytesseract
from PIL import Image


threadStop = False

bot = telebot.TeleBot(bottoken.TOKEN)  # You can set parse_mode by default. HTML or MARKDOWN
qbithost = 'http://localhost:8080/'
downloadTorrents = []

if sys.platform.startswith('win32'):
    # FreeBSD-specific code here...
    settingPath = 'APPDATA'
elif sys.platform.startswith('linux'):
    # Linux-specific code here...
    settingPath = 'HOME'

def imageToString(id, imagePathList):
    string = ""
    for imagePath in imagePathList:
        print(imagePath)
        # или вы можете использовать подушку
        image = Image.open(imagePath)
        # получаем строку
        string += pytesseract.image_to_string(image, lang='rus+eng')
    # печатаем
    if string != "":
        bot.send_message(id, string)
    return

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, '/qtinfo \n /qtDownloadInfo')


@bot.message_handler(commands=['qtinfo'])
def tor_info_message(message):
    startqtrnt()
    qb = Client(qbithost)
    qb.login(bottoken.QbUser, bottoken.QbPass)
    torrents = qb.torrents()
    for torrent in torrents:
        bot.send_message(message.chat.id, torrent['name'])
    qb.logout()


@bot.message_handler(commands=['qtDownloadInfo'])
def tor_info_message(message):
    startqtrnt()
    qb = Client(qbithost)
    qb.login(bottoken.QbUser, bottoken.QbPass)
    torrents = qb.torrents(filter='downloading')
    if not torrents:
        bot.send_message(message.chat.id, 'Нет не загруженных торрентов')
        return
    for torrent in torrents:
        bot.send_message(message.chat.id, torrent['name'])
    qb.logout()


@bot.message_handler(content_types='photo')
def photo_message(message):
    mes = "Прислано фото конвертирую ее в тескт"
    bot.send_message(message.chat.id, mes)
    slist = []
    for img in message.photo:
        print(img.file_size)
        unique_id = img.file_unique_id
        print(unique_id)
        if unique_id[len(unique_id)-1] != "-":
            continue
        file_id = img.file_id
        newFile = bot.get_file(file_id)

        src = config.DOWNLOADPATH + "/" + newFile.file_path
        print("thea "+src)
        filepath = os.path.exists(os.path.dirname(src))
        if not filepath:
            os.mkdir(os.path.dirname(src))
        downloaded_file = bot.download_file(newFile.file_path)

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        slist.append(src)
    imageToString(message.chat.id, slist)
    return

@bot.message_handler(content_types='document')
def torrent_message(message):
    print("Получен торрент файл")
    mes = 'Привет, ты прислал мне документ:' + message.document.file_name
    bot.send_message(message.chat.id, mes)
    if message.document.file_name.find(".torrent") > 0:
        file_id = message.document.file_id
        newFile = bot.get_file(file_id)

        filepath = os.path.exists(config.DOWNLOADPATH)
        if not filepath:
            os.mkdir(config.DOWNLOADPATH)
        downloaded_file = bot.download_file(newFile.file_path)

        # проверим запущен ли bittorrent
        startqtrnt()

        qb = Client(qbithost)
        qb.login(bottoken.QbUser, bottoken.QbPass)
        downTorrents = qb.torrents(filter='downloading')
        qb.download_from_file(downloaded_file)
        time.sleep(2)
        downAddedTorrents = qb.torrents(filter='downloading')
        findtorr = {}
        cont = False
        # поиск добавленного файла
        for addtorr in downAddedTorrents:
            for notaddtorr in downTorrents:
                if addtorr['name'] == notaddtorr['name']:
                    #downAddedTorrents.remove(addtorr)
                    #downTorrents.remove(notaddtorr)
                    cont = True
                    break
            if cont:
                cont = False
                continue
            findtorr = addtorr
            break

        if findtorr:
            downloadTorrents.append({'userid': message.chat.id, 'name': findtorr['name']})
        qb.logout()

    elif (message.document.file_name.find(".jpg") > 0) or (message.document.file_name.find(".png") > 0):
        mes = "Прислана картинка конвертирую ее в тескт"
        bot.send_message(message.chat.id, mes)
        file_id = message.document.file_id
        newFile = bot.get_file(file_id)

        src = config.DOWNLOADPATH + "/" + newFile.file_path
        filepath = os.path.exists(os.path.dirname(src))
        if not filepath:
            os.mkdir(os.path.dirname(src))
        downloaded_file = bot.download_file(newFile.file_path)

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        imageToString(message.chat.id, [src])
        return

    else:
        mes = "Прислан не тот документ"
        bot.send_message(message.chat.id, mes)
        return


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    mes = 'Веедена не верная команда: \"' + message.text + '\".'
    bot.reply_to(message, mes)

def startqtrnt():
    find_process = False
    for proc in psutil.process_iter():
        name = proc.name()
        if name.find(config.TORRENTCLIENTNAME) >= 0:
            find_process = True
            break
    # если торрент клиент не запщен то запускаем
    if not find_process:
        print("Запускаем торрент клиент")
        if sys.platform.startswith('win32'):
            os.startfile(config.TORRENTCLIENTPATH)
            #time.sleep(3)
        elif sys.platform.startswith('linux'):
            os.system("qbittorrent")
        time.sleep(10)


def handle_messages(messages):
    for message in messages:
        # Do something with the message
        if message.text[0] == '/':
            return
        bot.reply_to(message, 'Hi')


def thread_function(name):
    print("Поток запущен, бот работает")
    while True:
        if threadStop:
            # bot.stop_polling()
            print("Бот остановлен: поток")
            break
        try:
            bot.polling(none_stop=True)

        except Exception as e:
            print(e)
            print("Ошбика")
            time.sleep(3)


def thread_torr(name):
    print("Поток запущен, бот работает")
    while True:
        if threadStop:
            # bot.stop_polling()
            print("Бот остановлен: поток")
            break
        try:
            cont = False
            qb = Client(qbithost)
            qb.login(bottoken.QbUser, bottoken.QbPass)
            torrents = qb.torrents(filter='downloading')
            for dtor in downloadTorrents:
                for tor in torrents:
                    if tor['name'] == dtor['name']:
                        cont = True
                        break
                if cont:
                    cont = False
                    continue
                bot.send_message(dtor['userid'], "Файл " + dtor['name'] + "загружен")

            qb.logout()
            time.sleep(20)

        except Exception as e:
            print(e)
            print("Ошбика")
            time.sleep(3)

if __name__ == '__main__':
    botThread = threading.Thread(target=thread_function, args=(1,))
    threadStop = False
    botThread.start()
    sys.exit()
