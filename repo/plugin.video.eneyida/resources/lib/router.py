from urllib.parse import parse_qsl
from resources.lib.api import list_genres, list_videos, list_episodes, play_video

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