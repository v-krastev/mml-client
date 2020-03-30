"""
    Part of MML-client

    Exports class: Playlist
"""

import json
import logging
from pathlib import Path
from bin.song import Song
from bin._playlist_iter import PlaylistIterator


class Playlist:
    """
        Part of MML-client

        Instance methods:
            add_song(song)
            add_songs(songs_list)
            name()
            next_song()
            prev_song()
            remove_song(index)
            save(path)
            set_name(name)
            swap_songs(index_1, index_2)
            total_length()

        Static methods:
            load(path)
    """

    def __init__(self, name="Unknown"):
        """
        :param str name: The name of the Playlist.  default="Unknown"
        """

        self._name = name
        self.path = Path()
        self.songs = []
        self.current_song_index = -1

    def __eq__(self, other):
        """Two Playlist objects are equal, when their OS Paths are equal (they point to the same .json file)"""

        return self.path == other.path

    def __iter__(self):
        """
        :return PlaylistIterator object
        :rtype  PlaylistIterator
        """

        return PlaylistIterator(self)

    def __len__(self):
        """
        :return number of Song objects currently in the Playlist
        :rtype  int
        """

        return len(self.songs)

    def add_song(self, song):
        """
        Try to add a new Song to the Playlist

        If the Song object is already in the Playlist, fail silently

        :param song:
        :type  song: Song object

        :return True on success
        :rtype  Bool

        :raise TypeError if 'song' is not a Song object
        """

        if isinstance(song, Song):
            if song not in self.songs:
                self.songs.append(song)
                return True
            return False
        else:
            raise TypeError("Only MML-Song objects can be added to the Playlist!!!")

    def add_songs(self, songs_list):
        """
        Try to add a new list of Songs to the Playlist

        If any of the Song objects is already in the Playlist,
        skip silently and continue with the rest of the list

        :param songs_list:
        :type  songs_list: list of Song objects

        :return True if at least one Song was added
        :rtype  Bool

        :raise TypeError if anything from the 'songs_list' is not a Song object
        """

        added = False
        for song in songs_list:
            if isinstance(song, Song):
                if song not in self.songs:
                    self.songs.append(song)
                    added = True
            else:
                raise TypeError("Only MML-Song objects can be added to the Playlist!!!")
        return added

    @staticmethod
    def load(path):
        """
        Loads a PlayList from a specified JSON-Playlist file

        The file has to exists and should have an entry, indicating
        it's an MML-Playlist file (added by the Playlist.save() method)

        :param path: can be absolute or relative, but must point to a valid .json
        :type  path: Path
        :type  path: str

        :return a new Playlist or None
        :rtype  Playlist object or Bool

        :raise TypeError
        """

        # full OS-path to the Playlist file:
        path = Path(path).absolute().resolve().with_suffix(".json")

        new_playlist = Playlist("")

        if path.exists() and path.is_file():
            try:
                with open(path, 'r') as json_file:
                    data = json.load(json_file)

                    if "meta" in data and \
                            "Is MyLibrary Playlist" in data["meta"] and \
                            data["meta"]["Is MyLibrary Playlist"] == "yes":
                        logging.info("Loading MML-Playlist from: {}".format(path))

                        # to get rid of the PATH and from the '.json' part of the NAME:
                        new_playlist.set_name(path.stem)
                        new_playlist.path = path
                        for tmp_song in data["songs"]:
                            new_song = Song(tmp_song["title"],
                                            tmp_song["artist"],
                                            tmp_song["album"],
                                            tmp_song["length"],
                                            tmp_song["path"])
                            new_playlist.add_song(new_song)
                    else:
                        logging.warning("Not a valid MML-Playlist file: {}".format(path))
                        return None
            except Exception as e:
                logging.error("Could not read file: {}".format(path))
                return None

            logging.info("Playlist loaded successfully!")
            return new_playlist
        else:
            raise TypeError("Playlist.path must be a valid OS Path!")

    def name(self):
        """
        :return name
        :rtype  str
        """

        return str(self._name)

    def next_song(self):
        """
        Switch to the next song in the current Playlist

        If 'current_song_index' is at the LAST Song -> doing nothing
        Else -> changes the 'current_song_index' to the next Song

        :return 'current_song_index' (changed or not)
        :rtype  int
        """

        if len(self) != 0:
            if self.current_song_index < len(self) - 1:
                self.current_song_index += 1
        return self.current_song_index

    def prev_song(self):
        """
        Switch to the previous song in the current Playlist

        If 'current_song_index' is at the FIRST Song -> doing nothing
        Else -> changes the 'current_song_index' to the previous Song

        :return 'current_song_index' (changed or not)
        :rtype  int
        """

        if len(self) != 0:
            if self.current_song_index > 0:
                self.current_song_index -= 1
        return self.current_song_index

    def remove_song(self, index):
        """
        Remove the Song which is at the specified index

        If 'index' is in the Playlist boundaries ->
        delete the Song at index 'index'
        Modify the 'current_song_index' if needed
        Else -> doing nothing

        :param int index:

        :return True on success
        :rtype  Bool

        :raise TypeError
        """

        if isinstance(index, int):
            if 0 <= index < len(self):
                del self.songs[index]
                # if the last Song was previously marked and is now deleted:
                if self.current_song_index == len(self):
                    self.current_song_index -= 1
                return True
            return False
        else:
            raise TypeError("An index must be of type int!!!")

    def save(self, path):
        """
        Saves the Playlist to a specified DIRECTORY in a .json format

        Creates the .json file, its directory and their parents, if needed

        :param path:
        :type  path: Path
        :type  path: str

        :raise  TypeError
        """

        if isinstance(path, (str, Path)):
            path = Path(path).absolute().resolve()
            data = {"meta": {}, "songs": []}

            # create the os-PATH with any possible Parents, if not existent already:
            path.mkdir(parents=True, exist_ok=True)

            # create the string-PATH 'path/playlist_name.json':"""
            file_name = str(self._name).replace(' ', '-') + ".json"
            path = path.joinpath(file_name)

            # create the FILE 'path/playlist_name.json, if not existent already:
            path.touch(exist_ok=True)

            data["meta"].update({"Is MyLibrary Playlist": "yes"})
            # TODO: maybe not necessary?:
            data["meta"].update({"Path": str(path)})

            for song in self.songs:
                data["songs"].append({
                    "title": song.title(),
                    "artist": song.artist(),
                    "album": song.album(),
                    "length": song.length(),
                    "path": song.path()
                })

            with open(path, 'w') as json_file:
                logging.info("Saving MML-Playlist to: {}".format(path))
                json.dump(data, json_file, indent=2)
                logging.info("Playlist saved successfully!")

        else:
            raise TypeError("Playlist.path must be a valid OS Path!")

    def set_name(self, name):
        """
        Sets a new name for the current Playlist object

        :param str name:

        :return True on success
        :rtype  Bool

        :raise  TypeError
        """

        if isinstance(name, str) and name != "":
            self._name = name
            return True
        else:
            raise TypeError("Playlist.name must be a valid String!")

    def swap_songs(self, index_1, index_2):
        """
        Swap the Songs from the two indexes

        If 'index_1' and 'index_2' are in the Playlist boundaries ->
        swaps their places in the Playlist, NOT changing 'current_song_index'

        :return True on successful swap
        :return False otherwise (even indexes, or one of them is out of Playlist boundaries)
        :rtype  Bool

        :raise TypeError
        """

        if isinstance(index_1, int) and isinstance(index_2, int):
            if index_1 == index_2:
                return False
            elif index_1 < 0 or index_1 >= len(self.songs):
                return False
            elif index_2 < 0 or index_2 >= len(self.songs):
                return False
            else:
                songs_tuple = self.songs[index_1], self.songs[index_2]
                self.songs[index_2], self.songs[index_1] = songs_tuple
                return True
        else:
            raise TypeError("An index must be of type int!!!")

    def total_length(self):
        """
        Convert the total Songs length in a pretty-string

        :return hours:minutes:seconds
             or       minutes:seconds
             or              :seconds
             depending on how much the total length turns out to be
        :rtype  str
        """

        pretty_str = ""
        total_seconds = 0

        for song in self.songs:
            total_seconds += int(song.length())

        hours = total_seconds // 3600
        if hours > 0:
            pretty_str += str(hours) + ":"
            total_seconds %= 3600

        minutes = total_seconds // 60
        pretty_str += str(minutes)
        total_seconds %= 60

        if total_seconds < 10:
            pretty_str += ":0" + str(total_seconds)
        else:
            pretty_str += ":" + str(total_seconds)

        return pretty_str
