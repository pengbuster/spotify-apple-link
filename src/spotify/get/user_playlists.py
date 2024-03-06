from src.support.request_utils import open_request
from urllib.request import Request

ethan_user_id = 'snj7qqs5wyekwof6rkijdyzct'
access = 'BQCioTmiQU5SXF5IHjRqXa8X-KqJv4kYkeF0iQgcHHDAsZt5LA36P9Vxd56T1Fe7BkiRlcGsnUSA3qRHMjtwiiEwaLMwOzr1yBFUjtNGtqJwjsfsWNcCP1xxC7B9m3Mv42YTO9uLKSon7vEX58tD-1U3gOhYCv7w-XO9qcarHe-iwhWd950bxJcexloy_7JkA8NF6VyN4VzywYza8xAgfQ'


class Track:
    def __init__(self, name: str, artists: tuple, album: str):
        self._name = name
        self._artists = artists
        self._album = album

    def __str__(self):
        return f'{self._name}\n\tArtists: {self._artists}\n\tAlbum: {self._album}'

    def str_extra_tabs(self):
        return f'\t{self._name}\n\t\tArtists: {self._artists}\n\t\tAlbum: {self._album}'


class Playlist:
    def __init__(self, name: str, href: str):
        self._name = name
        self._href = href
        self._tracks = None

    def __str__(self):
        """
        Default string interpretation of Playlist object
        :return: String with playlist name on first line, and each Track underneath it indented with one tab character
        """
        to_string = self._name
        for track in self._tracks:
            to_string += f'\n{track.str_extra_tabs()}'
        return to_string

    def tracks(self, access_token: str) -> tuple[Track]:
        """
        Returns the tuple of Track objects representing each track in the Playlist
        Retrieves Track information from Spotify API if it hasn't been done for this playlist already
        :param access_token: Current access token to Spotify API with playlist owner's authorization and scope
            playlist-read-private and playlist-read-collaborative
        :return: Tuple of Tracks
        """
        # If tracks have not yet been retrieved, get tracks from Spotify
        if not self._tracks:
            # Endpoint URL for the specified playlist's tracks
            url = f'{self._href}/tracks'

            # Headers containing the access token to be sent with the request for playlist's tracks
            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            # Request to be used to obtain playlist's tracks
            request = Request(url=url, headers=headers)

            # Open the request and put the json response into response
            response = open_request(request)

            # Create the tuple of Tracks from the JSON response and put it in self._tracks
            self._tracks = tuple(_create_track_object(track) for track in response['items'])

        return self._tracks


def get_user_playlists(user_id: str, access_token: str) -> tuple[Playlist]:
    """
    Retrieves a dict of all playlists in the specified user's library and reformats as a tuple to return
    :param user_id: User ID of the user whose playlists are to be accessed. User ID can be found in the URL of the
        user's profile
    :param access_token: Access token with scope playlist-read-private and playlist-read-collaborative for the
        specified user
    :return: Tuple of Playlists
    """
    # Endpoint URL for the specified user's playlists
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'

    # Headers containing the access token to be sent with the request for user playlists
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Request to be opened to obtain user playlists
    request = Request(url=url, headers=headers)

    # Open the request and put the json response into response
    response = open_request(request)

    # Intermediary list object used to append Playlists to, will be converted to tuple to return
    playlists: list[Playlist] = []

    # Iterate all playlists in the json response (playlists are 'items')
    for playlist in response['items']:
        # Filtering out only the playlists that are owned by the specified user
        if playlist['owner']['id'] == user_id:
            # Add a Playlist object with its name and href to playlists list
            playlists.append(Playlist(playlist['name'], playlist['href']))

    # Return the tupleization of playlists list
    return tuple(playlists)


def _create_track_object(track: dict) -> Track:
    """
    Retrieves track name, artists, and album from a dict describing the track and returns a Track object with that data
    :param track: Dict of a track's info in a playlist from Spotify API JSON response
    :return: Correctly initialized Track object with name, artists' names tuple, and album name
    """
    name = track['track']['name']
    artists = tuple(artist['name'] for artist in track['track']['artists'])
    album = track['track']['album']['name']
    return Track(name=name, artists=artists, album=album)


if __name__ == '__main__':
    playlists = get_user_playlists(ethan_user_id, access)
    for playlist in playlists:
        playlist.tracks(access)
        print(playlist)
