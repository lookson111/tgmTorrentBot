import sys
DOWNLOADPATH = 'DownloadTorrent'
TORRENTCLIENTNAME = "qbitto"
SAVESETTINGSPATH = '%s/TelegramBot'
if sys.platform.startswith('win32'):
    # FreeBSD-specific code here...
    settingPath = 'APPDATA'
    TORRENTCLIENTPATH = "C:/Programms/qBittorrent/qbittorrent.exe"
elif sys.platform.startswith('linux'):
    # Linux-specific code here...
    settingPath = 'HOME'
    TORRENTCLIENTPATH = ""
    DOWNLOADPATH = 'DownloadTorrent'
