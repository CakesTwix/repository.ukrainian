import requests
import xbmcgui
import xbmcplugin
from bs4 import BeautifulSoup
import json
import sys
from urllib.parse import unquote

from resources.lib.constant import title_type
from resources.lib.utils import get_url, get_videos

# Get a plugin handle as an integer number.
HANDLE = int(sys.argv[1])


def list_videos(genre_index):
    """
    Create the list of playable videos in the Kodi interface.

    :param genre_index: the index of genre in the list of movie genres
    :type genre_index: int
    """
    genre_info = get_videos(genre_index)
    if genre_info["genre"] == "Пошук":
        keyb = xbmc.Keyboard("", "Пошук по сайту", False)
        keyb.doModal()

        if keyb.isConfirmed() and len(keyb.getText()) > 0:
            r = requests.post(
                "https://eneyida.tv/index.php?do=search",
                data={
                    "do": "search",
                    "subaction": "search",
                    "story": keyb.getText().replace(" ", "+"),
                },
            )
    else:
        r = requests.get(genre_info["url"])

    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, genre_info["genre"])
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, "movies")
    # Get the list of videos in the category.

    soup = BeautifulSoup(r.content, "html.parser")

    # Iterate through videos.
    for item in soup.find_all("article", class_="short"):
        # Create a list item with a text label
        list_item = xbmcgui.ListItem(label=genre_info["genre"])
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use only poster for simplicity's sake.
        # In a real-life plugin you may need to set multiple image types.
        list_item.setArt(
            {"poster": f"https://eneyida.tv{item.find('img')['data-src']}"}
        )
        # Set additional info for the list item via InfoTag.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType(genre_info["content"])
        info_tag.setTitle(item.find("a", class_="short_title").text)
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty("IsPlayable", "false")
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=https%3A%2F%2Fia600702.us.archive.org%2F3%2Fitems%2Firon_mask%2Firon_mask_512kb.mp4
        url = get_url(action="dubs", video=item.find("a", class_="short_title")["href"])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_NONE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)


def list_genres():
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


def list_dubs(title_url: str):
    """
    Create the list of playable episode in the Kodi interface.

    :param title_url: url content
    :type title_url: str
    """

    r = requests.get(title_url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, soup.find("h1").text)
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, "movie")
    list_item = xbmcgui.ListItem()
    # Get the list of videos in the category.

    plr = requests.get(soup.find("div", class_="video_box").find("iframe")["src"])
    plr_soup = BeautifulSoup(plr.content, "html.parser")
    # Parse as Movie
    if "/vod/" in soup.find("div", class_="video_box").find("iframe")["src"]:
        # Set additional info for the list item via InfoTag.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType("episodes")
        info_tag.setTitle(soup.find("h1").text)
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty("IsPlayable", "true")
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=https%3A%2F%2Fia600702.us.archive.org%2F3%2Fitems%2Firon_mask%2Firon_mask_512kb.mp4
        url = get_url(
            action="play",
            video=plr_soup.body.find("script", type="text/javascript")
            .text.split('file: "')[1]
            .split('",')[0],
        )
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    else:
        dubs = json.loads(
            plr_soup.body.find("script").text.split("file: '")[1].split("',")[0]
        )

        # Iterate through videos.
        for dub in dubs:  # Dubs, Season, Episode
            # Create a list item with a text label
            list_item = xbmcgui.ListItem(label=dub["title"])
            xbmcplugin.setContent(HANDLE, "movie")
            xbmcplugin.setPluginCategory(HANDLE, "Озвучення")
            xbmcplugin.addDirectoryItem(
                HANDLE,
                get_url(action="open_seasons", seasons_folder=dub["folder"]),
                list_item,
                True,
            )

    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_NONE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)


def open_seasons(seasons_folder):
    seasons = json.loads(unquote(seasons_folder).replace("'", '"'))
    if len(seasons) == 1:
        open_episodes(seasons[0]["folder"])
        return

    for season in json.loads(unquote(seasons_folder).replace("'", '"')):
        list_season = xbmcgui.ListItem(label=season["title"])
        xbmcplugin.setContent(HANDLE, "seasons")
        xbmcplugin.setPluginCategory(HANDLE, "Сезони")
        xbmcplugin.addDirectoryItem(
            HANDLE,
            get_url(action="open_episodes", episodes_folder=season["folder"]),
            list_season,
            True,
        )
        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_NONE)

    xbmcplugin.endOfDirectory(HANDLE)


def open_episodes(episodes_folder):
    for episode in json.loads(unquote(episodes_folder).replace("'", '"')):
        list_episode = xbmcgui.ListItem(label=episode["title"])
        list_episode.setArt({"poster": episode["poster"]})
        xbmcplugin.setContent(HANDLE, "episodes")
        xbmcplugin.setPluginCategory(HANDLE, "Епизоди")
        xbmcplugin.addDirectoryItem(
            HANDLE, get_url(action="play", video=episode["file"]), list_episode, False
        )
        xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_NONE)

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
