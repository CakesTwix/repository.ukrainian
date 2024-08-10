import os
from xbmcaddon import Addon
from xbmcvfs import translatePath

# Get addon base path
ADDON_PATH = translatePath(Addon().getAddonInfo("path"))
ICONS_DIR = os.path.join(ADDON_PATH, "resources", "images", "icons")
FANART_DIR = os.path.join(ADDON_PATH, "resources", "images", "fanart")

title_type = [
    {
        "genre": "Фільми",
        "content": "movies",
        "url": "https://eneyida.tv/films/",
        "icon": os.path.join(ICONS_DIR, "Movies.png"),
        "fanart": os.path.join(FANART_DIR, "Movies.png"),
    },
    {
        "genre": "Серіали",
        "content": "tvshows",
        "url": "https://eneyida.tv/series/",
        "icon": os.path.join(ICONS_DIR, "Shows.png"),
        "fanart": os.path.join(FANART_DIR, "Shows.png"),
    },
    {
        "genre": "Мультфільми",
        "content": "movies",
        "url": "https://eneyida.tv/cartoon/",
        "icon": os.path.join(ICONS_DIR, "CartoonMovies.png"),
        "fanart": os.path.join(FANART_DIR, "CartoonMovies.png"),
    },
    {
        "genre": "Мультсеріали",
        "content": "tvshows",
        "url": "https://eneyida.tv/cartoon-series/",
        "icon": os.path.join(ICONS_DIR, "Cartoon.png"),
        "fanart": os.path.join(FANART_DIR, "Cartoon.png"),
    },
    {
        "genre": "Аніме",
        "content": "tvshows",
        "url": "https://eneyida.tv/anime/",
        "icon": os.path.join(ICONS_DIR, "Anime.png"),
        "fanart": os.path.join(FANART_DIR, "Anime.png"),
    },
    {
        "genre": "Пошук",
        "content": "tvshows",
        "url": "https://eneyida.tv/index.php?do=search",
        "icon": os.path.join(ICONS_DIR, "Unknown.png"),
        "fanart": os.path.join(FANART_DIR, "Movies.png"),
    },
]