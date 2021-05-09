import sys
DOWNLOADPATH = 'D:/Downloads'
TORRENTCLIENTNAME = "qbitto"
SAVESETTINGSPATH = '%s/TelegramBot'
if sys.platform.startswith('win32'):
    # FreeBSD-specific code here...
    settingPath = 'APPDATA'
    TORRENTCLIENTPATH = "C:/Programms/qBittorrent/qbittorrent.exe"
elif sys.platform.startswith('linux'):
    # Linux-specific code here...
    settingPath = 'HOME'
    TORRENTCLIENTPATH = "C:/Programms/qBittorrent/qbittorrent.exe"
