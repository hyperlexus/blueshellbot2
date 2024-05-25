from Config.Exceptions import DeezerError, InvalidInput, SpotifyError, BlueshellError, YoutubeError
from Music.SpotifySearcher import SpotifySearch
from Music.DeezerSearcher import DeezerSearcher
from Utils.UrlAnalyzer import URLAnalyzer
from Config.Messages import SearchMessages
from Music.Downloader import Downloader
from Music.Types import Provider
from Utils.Utils import Utils


class Searcher:
    def __init__(self) -> None:
        self.__spotify = SpotifySearch()
        self.__deezer = DeezerSearcher()
        self.__messages = SearchMessages()
        self.__down = Downloader()

    async def search(self, track: str) -> list:
        provider = self.__identify_source(track)
        if provider == Provider.Unknown:
            raise InvalidInput(self.__messages.UNKNOWN_INPUT, self.__messages.UNKNOWN_INPUT_TITLE)

        elif provider == Provider.YouTube:
            try:
                track = self.__cleanYoutubeInput(track)
                songs = await self.__down.extract_info(track)
                return songs
            except BlueshellError as error:
                raise error
            except Exception as error:
                print(f'[Error in Searcher] -> {error}, {type(error)}')
                raise YoutubeError(self.__messages.YOUTUBE_NOT_FOUND, self.__messages.GENERIC_TITLE)

        elif provider == Provider.Spotify:
            try:
                songs = self.__spotify.search(track)
                if songs == None or len(songs) == 0:
                    raise SpotifyError(self.__messages.SPOTIFY_NOT_FOUND, self.__messages.GENERIC_TITLE)

                return songs
            except SpotifyError as error:
                raise error  # Redirect already processed error
            except Exception as e:
                print(f'[Spotify Error] -> {e}')
                raise SpotifyError(self.__messages.SPOTIFY_NOT_FOUND, self.__messages.GENERIC_TITLE)

        elif provider == Provider.Deezer:
            try:
                songs = self.__deezer.search(track)
                if songs == None or len(songs) == 0:
                    raise DeezerError(self.__messages.DEEZER_NOT_FOUND,
                                      self.__messages.GENERIC_TITLE)

                return songs
            except DeezerError as error:
                raise error  # Redirect already processed error
            except Exception as e:
                print(f'[Deezer Error] -> {e}')
                raise DeezerError(self.__messages.DEEZER_NOT_FOUND, self.__messages.GENERIC_TITLE)

        elif provider == Provider.Name:
            return [track]

    def __cleanYoutubeInput(self, track: str) -> str:
        trackAnalyzer = URLAnalyzer(track)
        # Just ID and List arguments probably
        if trackAnalyzer.queryParamsQuant <= 2:
            return track

        # Arguments used in Mix Youtube Playlists
        if 'start_radio' or 'index' in trackAnalyzer.queryParams.keys():
            return trackAnalyzer.getCleanedUrl()

    def __identify_source(self, track: str) -> Provider:
        if track == '':
            return Provider.Unknown

        if not Utils.is_url(track):
            return Provider.Name

        if "https://www.youtu" in track or "https://youtu.be" in track or "https://music.youtube" in track or "m.youtube" in track:
            return Provider.YouTube

        if "https://open.spotify.com" in track:
            return Provider.Spotify

        if "https://www.deezer.com" in track:
            return Provider.Deezer

        return Provider.Unknown
