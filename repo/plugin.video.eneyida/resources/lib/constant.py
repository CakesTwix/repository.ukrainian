import os
import requests
from xbmcaddon import Addon
from xbmcvfs import translatePath

addon = Addon()


def requests_no_ssl_verify(url):
    r = requests.get(url, verify=False)
    return r


# Get addon base path
ADDON_PATH = translatePath(addon.getAddonInfo("path"))
ICONS_DIR = os.path.join(ADDON_PATH, "resources", "images", "icons")
FANART_DIR = os.path.join(ADDON_PATH, "resources", "images", "fanart")
URL = f"https://{addon.getSetting('main_url')}"
MIRROR = f"https://{addon.getSetting('mirror')}"
main_url = URL if requests_no_ssl_verify(URL).status_code == 200 else MIRROR

title_type = [
    {
        "genre": "Фільми",
        "content": "movies",
        "url": f"{main_url}/films/",
        "icon": os.path.join(ICONS_DIR, "Movies.png"),
        "fanart": os.path.join(FANART_DIR, "Movies.png"),
    },
    {
        "genre": "Серіали",
        "content": "tvshows",
        "url": f"{main_url}/series/",
        "icon": os.path.join(ICONS_DIR, "Shows.png"),
        "fanart": os.path.join(FANART_DIR, "Shows.png"),
    },
    {
        "genre": "Мультфільми",
        "content": "movies",
        "url": f"{main_url}/cartoon/",
        "icon": os.path.join(ICONS_DIR, "CartoonMovies.png"),
        "fanart": os.path.join(FANART_DIR, "CartoonMovies.png"),
    },
    {
        "genre": "Мультсеріали",
        "content": "tvshows",
        "url": f"{main_url}/cartoon-series/",
        "icon": os.path.join(ICONS_DIR, "Cartoon.png"),
        "fanart": os.path.join(FANART_DIR, "Cartoon.png"),
    },
    {
        "genre": "Аніме",
        "content": "tvshows",
        "url": f"{main_url}/anime/",
        "icon": os.path.join(ICONS_DIR, "Anime.png"),
        "fanart": os.path.join(FANART_DIR, "Anime.png"),
    },
    {
        "genre": "Пошук",
        "content": "tvshows",
        "url": f"{main_url}/index.php?do=search",
        "icon": os.path.join(ICONS_DIR, "Unknown.png"),
        "fanart": os.path.join(FANART_DIR, "Movies.png"),
    },
]
