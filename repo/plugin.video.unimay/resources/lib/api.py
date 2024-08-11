import requests
import xbmcgui
import xbmcplugin
import json
import sys
from datetime import datetime

from resources.lib.constant import title_type
from resources.lib.utils import get_url, get_videos
from resources.lib.constant import IMAGES_URL, TITLE_URL

# Get a plugin handle as an integer number.
HANDLE = int(sys.argv[1])

###        Категории       ###
### Останні | Наші | Пошук ###
def list_category():
    """
    Create the list of movie genres in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, "Категории")
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, "movies")
    # Iterate through genres
    for index, genre_info in enumerate(title_type):
        # Create a list item with a text label.
        list_item = xbmcgui.ListItem(label=genre_info["genre"])
        # Set images for the list item.
        list_item.setArt({"icon": genre_info["icon"], "fanart": genre_info["fanart"]})
        # Set additional info for the list item using its InfoTag.
        # InfoTag allows to set various information for an item.
        # For available properties and methods see the following link:
        # https://codedocs.xyz/xbmc/xbmc/classXBMCAddon_1_1xbmc_1_1InfoTagVideo.html
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType("video")
        info_tag.setTitle(genre_info["genre"])
        info_tag.setGenres([genre_info["genre"]])
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&genre_index=0
        url = get_url(action="listing", genre_index=index)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)

    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_NONE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)

def list_latest(genre_index):
    genre_info = get_videos(genre_index)
    r_json = requests.get(genre_info["url"]).json()

    xbmcplugin.setPluginCategory(HANDLE, genre_info["genre"])

    xbmcplugin.setContent(HANDLE, "movies")

    for item in r_json:
        if item["series"]["premium"]: 
            continue
        list_item = xbmcgui.ListItem(label=genre_info["genre"])
        list_item.setInfo("video", {"plot": item["series"]["title"]})

        list_item.setArt(
            {
                "poster": f"{IMAGES_URL}{item['release']['posterUuid']}?width=640&format=webp",
                "fanart": f"{IMAGES_URL}{item['series']['imageUuid']}?width=2560&format=webp",
            },
        )

        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType(genre_info["content"])
        info_tag.setTitle(f'{item["release"]["name"]} Серія {item["series"]["number"]}')
        list_item.setProperty("IsPlayable", "false")

        url = get_url(
            action="episodes", video=item["release"]["code"]
        )

        is_folder = True
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)

    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(HANDLE)

def list_all(genre_index):
    genre_info = get_videos(genre_index)
    r_json = requests.get(genre_info["url"]).json()

    xbmcplugin.setPluginCategory(HANDLE, genre_info["genre"])

    xbmcplugin.setContent(HANDLE, "movies")

    for item in r_json["content"]:
        list_item = xbmcgui.ListItem(label=genre_info["genre"])
        list_item.setInfo("video", {"plot": item["description"]})

        list_item.setArt(
            {
                "poster": f"{IMAGES_URL}{item['images']['poster']}?width=640&format=webp",
                "fanart": f"{IMAGES_URL}{item['images']['banner']}?width=2560&format=webp",
                "logo": f"{IMAGES_URL}{item['images']['logo']}",
            },
        )

        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType(genre_info["content"])
        info_tag.setTitle(f'{item["names"]["ukr"]}')
        list_item.setProperty("IsPlayable", "false")

        url = get_url(
            action="open_title", video=item["code"]
        )

        is_folder = True
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)

    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(HANDLE)

def list_search(genre_index):
    pass

### Open Title ###

def load_title(title_url: str):
    """
    Create the list of playable episode in the Kodi interface.

    :param title_url: url content
    :type title_url: str
    """

    r_json = requests.get(f"{TITLE_URL}{title_url}").json()

    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, r_json["names"]["ukr"])
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, "tvshows")
    list_item = xbmcgui.ListItem(label="Епізоди")
    # Get the list of videos in the category.
    # Iterate through videos.
    for episode in r_json["playlist"]:
        if episode["premium"]: 
            continue
        info_tag = list_item.getVideoInfoTag()
        list_item.setArt({"poster": f"{IMAGES_URL}{episode['imageUuid']}"})
        # Set additional info for the list item via InfoTag.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType("episodes")
        info_tag.setGenres(r_json["genres"])
        info_tag.setTitle(
            f"{episode['number']}. {episode['title']}"
        )
        info_tag.setEpisode(episode["number"])
        info_tag.setDateAdded(str(datetime.fromtimestamp(int(episode["creationTimestamp"]) / 1000)))
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty("IsPlayable", "true")
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=https%3A%2F%2Fia600702.us.archive.org%2F3%2Fitems%2Firon_mask%2Firon_mask_512kb.mp4
        url = get_url(action="play", video=episode["hls"]["master"])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)

    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_NONE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)

def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    # offscreen=True means that the list item is not meant for displaying,
    # only to pass info to the Kodi player
    play_item = xbmcgui.ListItem(offscreen=True)
    play_item.setPath(path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)