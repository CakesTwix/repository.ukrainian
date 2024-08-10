# Copyright (C) 2023, Roman V. M.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Example video plugin that is compatible with Kodi 20.x "Nexus" and above
"""
import os
import sys
from urllib.parse import urlencode, parse_qsl

import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from xbmcvfs import translatePath

from bs4 import BeautifulSoup
import requests
import json

# Get the plugin url in plugin:// notation.
URL = sys.argv[0]
# Get a plugin handle as an integer number.
HANDLE = int(sys.argv[1])
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


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return "{}?{}".format(URL, urlencode(kwargs))


def get_genres():
    """
    Get the list of video genres

    Here you can insert some code that retrieves
    the list of video sections (in this case movie genres) from some site or API.

    :return: The list of video genres
    :rtype: list
    """
    return VIDEOS


def get_videos(genre_index):
    """
    Get the list of videofiles/streams.

    Here you can insert some code that retrieves
    the list of video streams in the given section from some site or API.

    :param genre_index: genre index
    :type genre_index: int
    :return: the list of videos in the category
    :rtype: list
    """
    return title_type[genre_index]


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
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)


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
        url = get_url(
            action="episodes", video=item.find("a", class_="short_title")["href"]
        )
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)


def list_episodes(title_url: str):
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
    list_item = xbmcgui.ListItem(label="Епізоди")
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
        # Iterate through videos.
        for dub in json.loads(
            plr_soup.body.find("script").text.split("file: '")[1].split("',")[0]
        ):  # Dubs, Season, Episode
            # Create a list item with a text label
            for season in dub["folder"]:
                for episode in season["folder"]:
                    info_tag = list_item.getVideoInfoTag()
                    # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
                    # Here we use only poster for simplicity's sake.
                    # In a real-life plugin you may need to set multiple image types.
                    list_item.setArt({"poster": episode["poster"]})
                    # Set additional info for the list item via InfoTag.
                    # 'mediatype' is needed for skin to display info for this ListItem correctly.
                    info_tag = list_item.getVideoInfoTag()
                    info_tag.setMediaType("episodes")
                    info_tag.setTitle(
                        f"{dub['title']} {season['title']} {episode['title']}"
                    )
                    # Set 'IsPlayable' property to 'true'.
                    # This is mandatory for playable items!
                    list_item.setProperty("IsPlayable", "true")
                    # Create a URL for a plugin recursive call.
                    # Example: plugin://plugin.video.example/?action=play&video=https%3A%2F%2Fia600702.us.archive.org%2F3%2Fitems%2Firon_mask%2Firon_mask_512kb.mp4
                    url = get_url(action="play", video=episode["file"])
                    # Add the list item to a virtual Kodi folder.
                    # is_folder = False means that this item won't open any sub-list.
                    is_folder = False
                    # Add our item to the Kodi virtual folder listing.
                    xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)

    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
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


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if not params:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_genres()
    elif params["action"] == "listing":
        # Display the list of videos in a provided category.
        list_videos(int(params["genre_index"]))
    elif params["action"] == "episodes":
        # Play a video from a provided URL.
        list_episodes(params["video"])
    elif params["action"] == "play":
        # Play a video from a provided URL.
        play_video(params["video"])
    else:
        # If the provided paramstring does not contain a supported action
        # we raise an exception. This helps to catch coding errors,
        # e.g. typos in action names.
        raise ValueError(f"Invalid paramstring: {paramstring}!")


if __name__ == "__main__":
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
