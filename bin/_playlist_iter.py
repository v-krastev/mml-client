class PlaylistIterator:
    """Iterator for class Playlist"""

    def __init__(self, playlist):
        self._songs = playlist.songs
        self._index = 0

    def __next__(self):
        if self._index < len(self._songs):
            song_obj = self._songs[self._index]
            self._index += 1
            return song_obj
        raise StopIteration
