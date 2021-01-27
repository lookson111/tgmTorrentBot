"""
    Написано Иматдиновым Ринатом
    работает на python 3.7.9
"""

import telebot
import config
import bottoken
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp
from PyQt5.QtCore import QSize
import sys
from mainwind import Ui_Dialog
import threading
import configparser
import psutil
from qbittorrent import Client

qb = Client('http://127.0.0.1:8080/')

threadStop = False
log = None

bot = telebot.TeleBot(bottoken.TOKEN)  # You can set parse_mode by default. HTML or MARKDOWN
downloadTorrents = []


class settingsBotCl:
    minimizeTray = "no"
    autostartBot = "no"
    downloadPath = ''

    # конструктор
    def __init__(self, dP):
        self.downloadPath = dP  # устанавливаем имя


settingsBot = settingsBotCl(config.DOWNLOADPATH)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, '/qtinfo \n /qtDownloadInfo')


@bot.message_handler(commands=['qtinfo'])
def tor_info_message(message):
    qb.login('admin', '1karina1')
    torrents = qb.torrents()
    for torrent in torrents:
        bot.send_message(message.chat.id, torrent['name'])
    qb.logout()


@bot.message_handler(commands=['qtDownloadInfo'])
def tor_info_message(message):
    qb.login('admin', '1karina1')
    torrents = qb.torrents(filter='downloading')
    if not torrents:
        bot.send_message(message.chat.id, 'Нет не загруженных торрентов')
        return
    for torrent in torrents:
        bot.send_message(message.chat.id, torrent['name'])
    qb.logout()


@bot.message_handler(content_types='document')
def torrent_message(message):
    if message.document.file_name.find(".torrent") < 0:
        mes = "Прислан не тот документ"
        bot.send_message(message.chat.id, mes)
        return
    mes = 'Привет, ты прислал мне документ:' + message.document.file_name
    bot.send_message(message.chat.id, mes)
    file_id = message.document.file_id
    newFile = bot.get_file(file_id)

    filepath = os.path.exists(config.DOWNLOADPATH)
    if not filepath:
        os.mkdir(config.DOWNLOADPATH)
    downloaded_file = bot.download_file(newFile.file_path)


    # src = message.document.file_name
    # with open(config.DOWNLOADPATH + "/" + src, 'wb') as new_file:
    #     new_file.write(downloaded_file)
    # mes = "Файл сохранен в " + config.DOWNLOADPATH
    # bot.send_message(message.chat.id, mes)

    # проверим запущен ли bittorrent
    find_process = False
    for proc in psutil.process_iter():
        name = proc.name()
        if name.find(config.TORRENTCLIENTNAME) >= 0:
            find_process = True
            break
    # если торрент клиент не запщен то запускаем
    if not find_process:
        os.startfile(config.TORRENTCLIENTPATH)
        time.sleep(3)
    qb.login('admin', '1karina1')
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


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    mes = 'Веедена не верная команда: \"' + message.text + '\".'
    bot.reply_to(message, mes)


def handle_messages(messages):
    for message in messages:
        # Do something with the message
        if message.text[0] == '/':
            return
        bot.reply_to(message, 'Hi')


def thread_function(name):
    log.append("Поток запущен, бот работает")
    while True:
        if threadStop:
            # bot.stop_polling()
            log.append("Бот остановлен: поток")
            break
        try:
            bot.polling(none_stop=True)

        except Exception as e:
            print(e)
            log.append("Ошбика")
            time.sleep(3)


def thread_torr(name):
    log.append("Поток запущен, бот работает")
    while True:
        if threadStop:
            # bot.stop_polling()
            log.append("Бот остановлен: поток")
            break
        try:
            cont = False
            qb.login('admin', '1karina1')
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
            log.append("Ошбика")
            time.sleep(3)


class MainWindow(QMainWindow):
    check_box = None
    tray_icon = None

    botThread = threading.Thread(target=thread_function, args=(1,))

    def __init__(self):
        QMainWindow.__init__(self)
        # super(MainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.startBot.clicked.connect(self.startBot)
        self.ui.stopBot.clicked.connect(self.stopBot)

        start_action = QAction("Start", self)
        stop_action = QAction('Stop', self)
        show_action = QAction("Show", self)
        hide_action = QAction("Hide", self)
        exit_action = QAction("Exit", self)

        start_action.triggered.connect(self.startBot)
        stop_action.triggered.connect(self.stopBot)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        exit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(start_action)
        tray_menu.addAction(stop_action)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(exit_action)
        # инициализация сворачивания в трей
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        global log
        log = self.ui.logTextBrowser

        # восстановление настроек
        self.loadSetting()
        if self.ui.autorunBotcheckBox.isChecked():
            self.startBot()

        if self.ui.trayCeckBox.isChecked():
            self.hide()
            self.tray_icon.showMessage(
                "Tray program",
                "Application is minimized to tray",
                QSystemTrayIcon.Information,
                2000
            )

    # переопредение метода closeEvent, для перехвата события закрытия окна
    # окно будет закрыватья только в том случае если нет, елси нет галочки на чекбосксе
    def closeEvent(self, event):
        self.stopBot()
        self.saveSettingss()

    def hideEvent(self, event):
        if self.ui.trayCeckBox.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Tray program",
                "Application is minimized to tray",
                QSystemTrayIcon.Information,
                2000
            )
        self.saveSettingss()

    def showEvent(self, event):
        self.show()

    def startBot(self):
        global threadStop
        threadStop = False
        self.botThread.start()
        self.ui.logTextBrowser.append('Бот запущен')

    def stopBot(self):
        global threadStop
        bot.stop_bot()
        threadStop = True
        self.ui.logTextBrowser.append('Бот остановлен')

    def saveSettingss(self):
        configp = configparser.ConfigParser()
        global settingsBot

        if self.ui.trayCeckBox.isChecked():
            settingsBot.minimizeTray = "yes"
        else:
            settingsBot.minimizeTray = "no"

        if self.ui.autorunBotcheckBox.isChecked():
            settingsBot.autostartBot = "yes"
        else:
            settingsBot.autostartBot = "no"

        configp['DEFAULT'] = {'minimizeToTray': settingsBot.minimizeTray,
                             'autostartBot': settingsBot.autostartBot,
                             'savePath': settingsBot.downloadPath}
        setdir = config.SAVESETTINGSPATH % os.environ['APPDATA']
        if not os.path.exists(setdir):
            os.mkdir(setdir)       
        setdir = setdir + '\\settings.ini'
        with open(setdir, 'w') as configfile:
            configp.write(configfile)

    def loadSetting(self):
        setdir = (config.SAVESETTINGSPATH % os.environ['APPDATA']) + '\\settings.ini'
        if not os.path.isfile(setdir):
            return
        configp = configparser.ConfigParser()
        try:
            configp.read(setdir)
        except Exception as e:
            os.remove(setdir)

        if configp.get("DEFAULT", "minimizeToTray") == "yes":
            self.ui.trayCeckBox.setChecked(True)
        if configp.get("DEFAULT", "autostartBot") == "yes":
            self.ui.autorunBotcheckBox.setChecked(True)
        self.ui.pathLineEdit.setText(configp.get("DEFAULT", "savePath"))


if __name__ == '__main__':
    # bot.infinity_polling()
    # bot.set_update_listener(handle_messages)
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
