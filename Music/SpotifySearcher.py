from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
from Config.Exceptions import SpotifyError
from Config.Configs import BConfigs
from Config.Messages import SpotifyMessages


class SpotifySearch:
    def __init__(self) -> None:
        self.__messages = SpotifyMessages()
        self.__config = BConfigs()
        self.__connected = False
        self.__connect()

    def __connect(self) -> None:
        try:
            auth = SpotifyClientCredentials(self.__config.SPOTIFY_ID, self.__config.SPOTIFY_SECRET)
            self.__api = Spotify(auth_manager=auth)
            self.__connected = True
        except Exception as e:
            print(f'DEVELOPER NOTE -> Spotify Connection Error {e}')

    def search(self, url: str) -> list:
        if not self.__checkUrlValid(url):
            raise SpotifyError(self.__messages.INVALID_SPOTIFY_URL, self.__messages.GENERIC_TITLE)

        song_type = url.split('/')[3].split('?')[0]
        code = url.split('/')[4].split('?')[0]
        songs = []

        try:
            if self.__connected:
                match song_type:
                    case 'album':
                        songs = self.__get_album(code)
                    case 'playlist':
                        songs = self.__get_playlist(code)
                    case 'track':
                        songs = self.__get_track(code)
                    case 'artist':
                        songs = self.__get_artist(code)

            if self.__connected:
                match song_type:
                    case 'album':
                        self.__get_album(code)
                    case 'playlist':
                        self.__get_playlist(code)
                    case 'track':
                        self.__get_track(code)
                    case 'artist':
                        self.__get_artist(code)

                # ↓ this will stay here as a testiment to my lack of brain ↓
                # if type == 'album' or 'playlist' or 'track' or 'artist':
                #     eval(f'self.__get_{song_type}(code)')

            return songs
        except SpotifyException:
            raise SpotifyError(self.__messages.INVALID_SPOTIFY_URL, self.__messages.GENERIC_TITLE)

    def __get_album(self, code: str) -> list:
        results = self.__api.album_tracks(code)
        songs = results['items']

        while results['next']:  # Get the next pages
            results = self.__api.next(results)
            songs.extend(results['items'])

        songsTitle = []

        for music in songs:
            title = self.__extract_title(music)
            songsTitle.append(title)

        return songsTitle

    def __get_playlist(self, code: str) -> list:
        results = self.__api.playlist_items(code)
        itens = results['items']

        while results['next']:  # Load the next pages
            results = self.__api.next(results)
            itens.extend(results['items'])

        songs = []
        for item in itens:
            songs.append(item['track'])

        titles = []
        for music in songs:
            title = self.__extract_title(music)
            titles.append(title)

        return titles

    def __get_track(self, code: str) -> list:
        results = self.__api.track(code)
        name = results['name']
        artists = ''
        for artist in results['artists']:
            artists += f'{artist["name"]} '

        return [f'{name} {artists}']

    def __get_artist(self, code: str) -> list:
        results = self.__api.artist_top_tracks(code, country='BR')

        songs_titles = []
        for music in results['tracks']:
            title = self.__extract_title(music)
            songs_titles.append(title)

        return songs_titles

    def __extract_title(self, music: dict) -> str:
        title = f'{music["name"]} '
        for artist in music['artists']:
            title += f'{artist["name"]} '

        return title

    def __checkUrlValid(self, url: str) -> bool:
        try:
            type = url.split('/')[3].split('?')[0]
            code = url.split('/')[4].split('?')[0]

            if type == '' or code == '':
                return False

            return True
        except:
            return False
