# tgmTorrentBot
install modules:
pip3 install pytelegrambotapi psutil python-qbittorrent pytesseract

установить
tesseract

создать файл bottoken
TOKEN = 'записать токен телеграмм бота'
QbUser = 'имя юсера на веб qb'
QbPass = 'пароль на веб qb'

Автозапуск Linux
Через "Автоматически запускаемые приложения"
("Alt+F2" and run the "gnome-session-properties") добавить
/usr/bin/python3.8 /home/server/py/tgmTorrentBot/main.py
qbittorrent
