from urllib.parse import parse_qsl
from resources.lib.api import list_category, list_latest, load_title, list_all, play_video

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
        # Main
        list_category()
    elif params["action"] == "listing":
        if int(params["genre_index"]) == 0:
            list_latest(0)
        elif int(params["genre_index"]) == 1:
            list_all(1)

    # Open title
    elif params["action"] == "open_title":
        # Play a video from a provided URL.
        load_title(params["video"])
    elif params["action"] == "play":
        # Play a video from a provided URL.
        play_video(params["video"])
    else:
        # If the provided paramstring does not contain a supported action
        # we raise an exception. This helps to catch coding errors,
        # e.g. typos in action names.
        raise ValueError(f"Invalid paramstring: {paramstring}!")