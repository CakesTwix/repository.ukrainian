import os
from xbmcaddon import Addon
from xbmcvfs import translatePath

# Get addon base path
ADDON_PATH = translatePath(Addon().getAddonInfo("path"))
IMAGES_DIR = os.path.join(ADDON_PATH, "resources", "images")
ICONS_DIR = os.path.join(ADDON_PATH, "resources", "images", "icons")
FANART_DIR = os.path.join(ADDON_PATH, "resources", "images", "fanart")

API_URL = "https://api.unimay.media"
FIND_URL = f"{API_URL}/v1/release/search?title="
TITLE_URL = f"{API_URL}/v1/release?code="
IMAGES_URL = "https://img.unimay.media/"

title_type = [
    {
        "genre": "Останні релізи",
        "content": "tvshows",
        "url": f"{API_URL}/v1/list/series/updates?size=15",
        "icon": os.path.join(ICONS_DIR, "Anime.png"),
        "fanart": os.path.join(IMAGES_DIR, "fanart.png"),
    },
    {
        "genre": "Наші проєкти",
        "content": "tvshows",
        "url": f"{API_URL}/v1/release/search?page_size=30&page=0",
        "icon": os.path.join(ICONS_DIR, "Anime.png"),
        "fanart": os.path.join(IMAGES_DIR, "fanart.png"),
    },
    {
        "genre": "Пошук",
        "content": "tvshows",
        "url": f"{FIND_URL}",
        "icon": os.path.join(ICONS_DIR, "Anime.png"),
        "fanart": os.path.join(IMAGES_DIR, "fanart.png"),
    },
]