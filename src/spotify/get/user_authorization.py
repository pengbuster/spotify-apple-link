import random
import string
import webbrowser

from urllib.parse import urlencode

client_id = 'dafa9790e6614a4fbbe9fc778f8f1902'
redirect_uri = 'http://localhost'

'''
http://localhost/
?code=AQAyhSGnxk2ifc2f9SPXe60raP_iDmzQVdSLM7rRf-MJFl3_SWl_jbB43kR4VgFhll74EKkRCfxvC90uyURKWQLpMYrdjs-TU_arxUAST64G1yCXoiQ8OzbWWR7dH19FxpwbzyNplelrgqBaPkfl2m3xTF5R-VarFoAwZlf_Hj9RRZhto6IZxN2rI20cQULHVgDxDSJq7j2wwxkpXAi--mnQcBG9Npbl
&state=_O%5D%3F0W%23pgpVEn%3AT2
'''


def get_user_authorization() -> None:
    """
    Prompts to open the default web browser to gain an authorization code in order to access user account
    :return: None - Authorization code must be retrieved from webpage redirect
    """
    # Base url for Spotify's user authorization
    base_url = 'https://accounts.spotify.com/authorize?'

    # Query parameters for user authorization URL
    query = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': _generate_random_string(16),
        'scope': 'playlist-read-private playlist-read-collaborative'
    }

    # Open up full url in default web browser (base_url + query parameters)
    webbrowser.open(base_url + urlencode(query))


def _generate_random_string(length) -> str:
    """
    Generates a random string of specified length
    :param length: character count of generated string
    :return: Generated random string
    """
    # List of all characters that random string can be composed of
    chars = string.ascii_letters + string.digits + string.punctuation

    # Choose a random char in chars length times and join them together and return
    return ''.join(random.choice(chars) for _ in range(length))


if __name__ == '__main__':
    get_user_authorization()
