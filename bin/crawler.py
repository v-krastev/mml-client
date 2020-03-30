import logging
from pathlib import Path
from bin.playlist import Playlist
from bin.song import Song


class Crawler:
    def __init__(self):
        pass

    @classmethod
    def find_songs(cls, path, file_type=None):
        """ Scans the specified 'path'' and returns a list
            of Song-objects of supported types

            USAGE:  pl = Playlist(pl_name)
                    pl.add_songs(crawler.find_songs(path_to_songs))"""

        path = Path(path).absolute().resolve()
        found_songs = list()

        if path.exists() and path.is_dir():
            supported_types = [".mp3"]

            # if "file_type" is not specified,
            # all supported types are checked:
            if file_type is None:
                file_type = supported_types
            elif file_type not in supported_types:
                logging.error("Supplied file-type not supported by MML_client: {}".format(file_type))

            # Get all the 'objects' in the specified 'path'
            # which are 'files' (not dirs) and iterate over them
            # it is NON-Recursive and with dept==1:
            for file in [obj for obj in path.iterdir() if obj.is_file()]:
                if file.suffix in file_type:
                    temp_song = Song().load(file)
                    if temp_song is not None:
                        found_songs.append(temp_song)

        return found_songs

    @classmethod
    def find_playlist(cls, path):
        """ Scans the specified 'path' and returns a list
            of Playlist-objects """

        path = Path(path).absolute().resolve()
        playlists = list()

        if path.exists() and path.is_dir():
            logging.info("Searching for MML-Playlists in {}: ".format(path))

            # Get all the 'objects' in the specified 'path'
            # which are 'files' (not dirs) and iterate over them
            # it is NON-Recursive and with dept==1:
            for file in [obj for obj in path.iterdir() if obj.is_file()]:
                if file.suffix == ".json":
                    tmp_playlist = Playlist.load(file)
                    if tmp_playlist.name() != "":
                        playlists.append(tmp_playlist)
        else:
            logging.error("Could not open the path: {}".format(path))
        return playlists
