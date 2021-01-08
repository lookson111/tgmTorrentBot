import telebot
import config
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QCheckBox, QSystemTrayIcon, \
    QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp
from PyQt5.QtCore import QSize
import sys
from mainwind import Ui_Dialog

bot = telebot.TeleBot(config.TOKEN)  # You can set parse_mode by default. HTML or MARKDOWN


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(content_types='document')
def start_message(message):
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
    src = message.document.file_name
    with open(config.DOWNLOADPATH + "/" + src, 'wb') as new_file:
        new_file.write(downloaded_file)
    mes = "Файл сохранен в " + config.DOWNLOADPATH
    bot.send_message(message.chat.id, mes)


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


class MainWindow(QMainWindow):
    check_box = None
    tray_icon = None
    def __init__(self):
        QMainWindow.__init__(self)
        #super(MainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        show_action = QAction("Show", self)
        hide_action = QAction("Hide", self)
        exit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        exit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(exit_action)
        # инициализация сворачивания в трей
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()


    # переопредение метода closeEvent, для перехвата события закрытия окна
    # окно будет закрыватья только в том случае если нет, елси нет галочки на чекбосксе
    def closeEvent(self, event):
        if self.ui.trayCeckBox.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Tray program",
                "Application is minimized to tray",
                QSystemTrayIcon.Information,
                2000
            )

if __name__ == '__main__':
    # bot.infinity_polling()
    # bot.set_update_listener(handle_messages)
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
    # while True:
    #     try:
    #         bot.polling(none_stop=True)
    #
    #     except Exception as e:
    #         print(e)
    #         time.sleep(3)

