from Tests.TestBase import BlueshellTesterBase
from Config.Exceptions import SpotifyError


class BlueshellSpotifyTest(BlueshellTesterBase):
    def __init__(self) -> None:
        super().__init__()

    def test_spotifyTrack(self) -> bool:
        songs = self._runner.run_coroutine(
            self._searcher.search(self._constants.SPOTIFY_TRACK_URL))

        if len(songs) > 0:
            return True
        else:
            return False

    def test_spotifyPlaylist(self) -> bool:
        songs = self._runner.run_coroutine(
            self._searcher.search(self._constants.SPOTIFY_PLAYLIST_URL))

        if len(songs) > 0:
            return True
        else:
            return False

    def test_spotifyArtist(self) -> bool:
        songs = self._runner.run_coroutine(
            self._searcher.search(self._constants.SPOTIFY_ARTIST_URL))

        if len(songs) > 0:
            return True
        else:
            return False

    def test_spotifyAlbum(self) -> bool:
        songs = self._runner.run_coroutine(
            self._searcher.search(self._constants.SPOTIFY_ARTIST_URL))

        if len(songs) > 0:
            return True
        else:
            return False

    def test_spotifyWrongUrlShouldThrowException(self) -> bool:
        try:
            songs = self._runner.run_coroutine(
                self._searcher.search(self._constants.SPOTIFY_WRONG1_URL))

        except SpotifyError as e:
            print(f'Spotify Error -> {e.message}')
            return True
        except Exception as e:
            print(e)
            return False

    def test_spotifyWrongUrlTwoShouldThrowException(self) -> bool:
        try:
            songs = self._runner.run_coroutine(
                self._searcher.search(self._constants.SPOTIFY_WRONG2_URL))

        except SpotifyError as e:
            print(f'Spotify Error -> {e.message}')
            return True
        except Exception as e:
            return False
