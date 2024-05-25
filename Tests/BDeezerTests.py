from Tests.TestBase import BlueshellTesterBase
from Config.Exceptions import DeezerError


class BlueshellDeezerTest(BlueshellTesterBase):
    def __init__(self) -> None:
        super().__init__()

    def test_deezerTrack(self) -> bool:
        songs = self._runner.run_coroutine(
            self._searcher.search(self._constants.DEEZER_TRACK_URL))

        if len(songs) > 0:
            return True
        else:
            return False

    def test_deezerPlaylist(self) -> bool:
        songs = self._runner.run_coroutine(
            self._searcher.search(self._constants.DEEZER_PLAYLIST_URL))

        if len(songs) > 0:
            return True
        else:
            return False

    def test_deezerArtist(self) -> bool:
        songs = self._runner.run_coroutine(
            self._searcher.search(self._constants.DEEZER_ARTIST_URL))

        if len(songs) > 0:
            return True
        else:
            return False

    def test_deezerAlbum(self) -> bool:
        songs = self._runner.run_coroutine(
            self._searcher.search(self._constants.DEEZER_ALBUM_URL))

        if len(songs) > 0:
            return True
        else:
            return False

    def test_deezerWrongUrlShouldThrowException(self) -> bool:
        try:
            songs = self._runner.run_coroutine(
                self._searcher.search(self._constants.DEEZER_WRONG1_URL))

        except DeezerError as e:
            print(f'Deezer Error -> {e.message}')
            return True
        except Exception as e:
            print(e)
            return False

    def test_deezerWrongUrlTwoShouldThrowException(self) -> bool:
        try:
            songs = self._runner.run_coroutine(
                self._searcher.search(self._constants.DEEZER_WRONG2_URL))

        except DeezerError as e:
            print(f'Deezer Error -> {e.message}')
            return True
        except Exception as e:
            return False
