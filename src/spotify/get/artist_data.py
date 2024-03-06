import urllib.parse
import urllib.request

from src.support.request_utils import open_request


def get_artist_data() -> None:
    """
    Prompts the user for a console inputted Spotify API access code and retrieves an artist's data from the API
    :return: None, artist data is printed to the console
    """
    # Builds the request for artist data with console inputted access token
    request = _build_request()

    # Open request and store the JSON response into response
    response = open_request(request)

    # Print artist data
    print(response)


def _build_request() -> urllib.request.Request:
    """
    Builds the request for an artist's data yet to be sent to Spotify web API
    :return: Unopened Request object for an artist's data with console inputted access code
    """
    access_token = _get_access_token()

    # Hardcoded URL for Coldplay
    url = 'https://api.spotify.com/v1/artists/4gzpq5DPGxSnKTe4SA8HAU'

    # Access token as the header, Spotify states format should be "Bearer  {access_token}"
    headers = {
        'Authorization': f'Bearer  {access_token}'
    }

    return urllib.request.Request(url=url, headers=headers)


def _get_access_token() -> str:
    """
    Used to get the client's access token
    :return: User inputted value into the console
    """
    return input('Access Token: ').strip()
