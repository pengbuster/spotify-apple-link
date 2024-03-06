from base64 import b64encode
from datetime import datetime, timedelta
from enum import Enum
from src.support.request_utils import open_request
from urllib.parse import urlencode
from urllib.request import Request

client_id = 'dafa9790e6614a4fbbe9fc778f8f1902'
client_secret = 'aee163dfb07b4baaaa33c00a7deeb111'
client_info_encoded = b64encode(f'{client_id}:{client_secret}'.encode()).decode()

access_token = 'AQAyhSGnxk2ifc2f9SPXe60raP_iDmzQVdSLM7rRf-MJFl3_SWl_jbB43kR4VgFhll74EKkRCfxvC90uyURKWQLpMYrdjs-TU_arxUAST64G1yCXoiQ8OzbWWR7dH19FxpwbzyNplelrgqBaPkfl2m3xTF5R-VarFoAwZlf_Hj9RRZhto6IZxN2rI20cQULHVgDxDSJq7j2wwxkpXAi--mnQcBG9Npbl'
refr_token = 'AQB0hr1VMRWjrHD09ra7X6acL59resznbVansnQNsdpudZd_vmgpnNn4AoVRQ8lHZKGSVcqrwV4jUeyezIMCiyTsi7mXfae_Kb8sIH9JcpzyULwHoklNf8bFM0hEVfnkVpQ'


class AccessTokenKind(Enum):
    GENERAL = 'GENERAL'
    USERAUTH = 'USERAUTH'
    REFRESH = 'REFRESH'


def get_access_token(kind: AccessTokenKind, /, auth_code: str = None, refresh_token: str = None):
    """
    Sends a request to Spotify API with a client id and secret and prints the access token and expiration time to the
        console
    :param kind: AccessTokenKind class that defines what type of access token will be retrieved from Spotify API
    :param auth_code: Authorization code for Spotify user's info
    :param refresh_token: Refresh token for a Spotify user's authorization
    :return: None - access token and expiration time will be printed to console
    """
    # Setting parameters for request to Spotify API
    url = 'https://accounts.spotify.com/api/token'
    data, headers = _build_data_and_headers(kind, auth_code, refresh_token)

    # Constructing Request to send to Spotify API
    request = Request(url=url, data=data, headers=headers)

    # Open request and put its json contents into response
    response = open_request(request)

    # Print access code and its expiration time
    print(response)
    print('\n')
    print(f"Access Token: {response['access_token']}")
    _print_expiration_time(response['expires_in'])


def _build_data_and_headers(kind: AccessTokenKind, auth_code: str, refresh_token: str) -> (str, dict[str]):
    """
    Constructs and returns the data and headers to be used in the Spotify API Request
    :param kind:
    :param auth_code: Authorization code used for playlist access token
    :return: A tuple containing the URL encoded data and a dict of URL headers
    """
    data = None
    headers = {}

    # Depending on the type of access token to be requested, set the data and headers to their appropriate values
    # See Spotify API documentation for detailed data and header requirements
    if kind == AccessTokenKind.GENERAL:
        data = urlencode({
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }).encode('utf-8'),
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    elif kind == AccessTokenKind.USERAUTH:
        data = urlencode({
            'code': auth_code,
            'redirect_uri': 'http://localhost',
            'grant_type': 'authorization_code',
        }).encode('utf-8'),
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {client_info_encoded}',
        }
    elif kind == AccessTokenKind.REFRESH:
        data = urlencode({
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }).encode('utf-8'),
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {client_info_encoded}',
        }

    return data, headers


def _print_expiration_time(expires_in: int) -> None:
    """
    Prints the time when the associated Spotify API access token will expire
    :param expires_in: Number of seconds from current time when the access token will expire
    :return: None - expiration time will be printed to the console
    """
    # Get current datetime, add expires_in in seconds to current_time, then print the resulting datetime
    current_time = datetime.now()
    time_delta = timedelta(seconds=expires_in)
    expire_time = current_time + time_delta
    print(f'Access token expiration time: {expire_time}')


if __name__ == '__main__':
    get_access_token(AccessTokenKind.REFRESH,
                     refresh_token='AQB0hr1VMRWjrHD09ra7X6acL59resznbVansnQNsdpudZd_vmgpnNn4AoVRQ8lHZKGSVcqrwV4jUeyezIMCiyTsi7mXfae_Kb8sIH9JcpzyULwHoklNf8bFM0hEVfnkVpQ')
