"""
    Part of MML-client

    Exports class: Song
"""

from datetime import time
import logging
from pathlib import Path
from mutagen import MutagenError
from mutagen.mp3 import EasyMP3


class Song:
    """
        Part of MML-client

        Does NOT contain the actual audio file, only its Path

        Instance methods:
            album()
            artist()
            length()
            length_pretty(hours=False, minutes=False, seconds=False)
            path()
            title()
            set_album(album)
            set_artist(artist)
            set_length(length)
            set_path(path)
            set_title(title)

        Static methods:
            load(path)
    """

    def __init__(self, title="Unknown", artist="Unknown", album="Unknown", length="0", path=""):
        """
        :param str title:  The title of the Song.               default = "Unknown"

        :param str artist: The artist of the Song.              default = "Unknown"

        :param str album:  The album of the Song.               default = "Unknown"

        :param length:     The length of the Song in seconds.   default = "0"
        :type  length: str
        :type  length: int
        If type is 'str', the value should be the seconds,
        an 'int' convertible (only digits)

        :param path:   The path of the actual audio file.   default = ""
        :type  path: str
        :type  path: Path
        """

        self._title = ""
        self.set_title(title)
        self._artist = ""
        self.set_artist(artist)
        self._album = ""
        self.set_album(album)
        self._length = time(hour=0, minute=0, second=0)
        self.set_length(length)
        self._path = Path(path).absolute().resolve()

    def __bool__(self):
        """
        Currently only checks if all of the attributes are set.
        """

        if self._title and self._artist and self._album and self._length and self._path:
            return True
        return False

    def __eq__(self, song):
        """Two Song objects are equal, when their OS Paths are equal (they point to the same audio file)"""
        return self.path() == song.path()

    def album(self):
        """
        :return album
        :rtype  str
        """

        return str(self._album)

    def artist(self):
        """
        :return artist
        :rtype  str
        """

        return str(self._artist)

    def length(self):
        """
        For use when writing (saving) to a Playlist file

        Converts the inner 'time' object representing the
        'length' attribute to a 'str' object of the length in seconds

        :return length
        :rtype  str
        """

        seconds = 0
        if self._length.second:
            seconds += self._length.second
        if self._length.minute:
            seconds += self._length.minute * 60
        if self._length.hour:
            seconds += self._length.minute * 60
        return str(seconds)

    @staticmethod
    def _length_from_str(seconds):
        """
        Internal use
        """

        hours = seconds // 3600

        seconds %= 3600
        minutes = seconds // 60

        seconds %= 60

        return time(hour=hours, minute=minutes, second=seconds)

    def length_pretty(self, hours=False, minutes=False, seconds=False):
        """
        Create a pretty string representation of the length of the Song

        If All parameters are False -> the full length is returned
        Else -> only the ones who are True

        :param Bool hours:   explicitly use the hours
        :param Bool minutes: explicitly use the minutes
        :param Bool seconds: explicitly use the seconds

        :return hours:minutes:seconds -> Everything is False or Everything is True
             or       minutes:seconds -> Only 'seconds' and 'minutes' are True
             or              :seconds -> Only 'seconds' is True
        :rtype  str
        """

        str_time = ""
        if hours:
            str_time += str(self._length.hour) + ":"
        if minutes:
            if self._length.minute < 10:
                str_time += "0"
            str_time += str(self._length.minute)
        if seconds:
            if self._length.second < 10:
                str_time += ":0" + str(self._length.second)
            else:
                str_time += ":" + str(self._length.second)
        if str_time == "":
            str_time = "{}:{}:{}".format(self._length.hour, self._length.minute, self._length.second)
        return str_time

    @staticmethod
    def load(path):
        """
        Loads a Song object from the given path

        :param path:
        :type  path: str
        :type  path: Path

        :return the newly loaded Song or None if could not read the audio file
        :rtype  Song object
        :rtype  Bool

        :raise TypeError when 'path' is not a String or a Path
        :raise ValueError when 'path' is resolved to a Directory or a non-existent location
        """

        if not isinstance(path, (str, Path)):
            raise TypeError("Song.path must be a valid OS Path or a Path-convertible String!")
        else:
            path = Path(path).absolute().resolve()

        if not path.exists() or not path.is_file():
            raise ValueError("Song.path must be a valid OS File-Path or a Path-convertible String!")

        try:
            temp_song = Song()
            audio_file = EasyMP3(path)

            if audio_file is not None and audio_file.tags is not None:
                # NOTE: the '[0]' in 'song_file.tags[...][0]'
                # is because the default return value is a single-item LIST.
                # This way, we avoid the '[...]' brackets in the Song's attributes
                if "title" in audio_file.tags:
                    temp_song.set_title(str(audio_file.tags["title"][0]))
                else:
                    temp_song.set_title(path.stem)

                if "artist" in audio_file.tags:
                    temp_song.set_artist(str(audio_file.tags["artist"][0]))

                if "album" in audio_file.tags:
                    temp_song.set_album(str(audio_file.tags["album"][0]))

                if temp_song.length() == "0":
                    temp_song.set_length(audio_file.info.length)

                temp_song.set_path(path)

                logging.info("Audio file loaded: {}".format(temp_song.path()))
                return temp_song

        except MutagenError as e:
            logging.error("Audio file could NOT be loaded: {}"
                          "Error: {}".format(path, e))
        return None

    def path(self):
        """
        :return path
        :rtype  str
        """

        return str(self._path)

    def title(self):
        """
        :return title
        :rtype  str
        """

        return str(self._title)

    def set_album(self, album):
        """
        Sets a new album for the current Song object

        :param str album:

        :return True on success
        :rtype  Bool

        :raise TypeError when 'album' is not a String
        :raise ValueError when 'album' is an empty String
        """

        if not isinstance(album, str):
            raise TypeError("Song.album must be a valid String!")
        elif album == "":
            raise ValueError("Song.album cannot be an empty String!")
        else:
            self._album = album
            return True

    def set_artist(self, artist):
        """
        Sets a new artist for the current Song object

        :param str artist:

        :return True on success
        :rtype  Bool

        :raise TypeError when 'artist' is not a String
        :raise ValueError when 'artist' is an empty String
        """

        if not isinstance(artist, str):
            raise TypeError("Song.artist must be a valid String!")
        elif artist == "":
            raise ValueError("Song.artist cannot be an empty String!")
        else:
            self._artist = artist
            return True

    def set_length(self, length):
        """
        Sets a new length for the current Song object

        :param length:
        :type  length: str int

        :return True on success
        :rtype  Bool

        :raise TypeError when 'length' is not a String, Int or Float
        :raise ValueError when 'length' is converted to a negative Int
        """

        try:
            if not isinstance(length, bool):
                # cast to 'float' to allow inputs such as str("5.14"):
                length = float(length)
            else:
                raise TypeError
        except TypeError:
            raise TypeError("Song.length must be a valid Int, Float or an Int-parsable String!")

        if length < 0:
            raise ValueError("Song.length cannot be a negative value!")
        else:
            self._length = self._length_from_str(int(length))
        return True

    def set_path(self, path):
        """
        Sets a new Path for the current Song object

        :param path:
        :type  path: str Path

        :return True on success
        :rtype  Bool

        :raise TypeError when 'path' is not a String or Path
        :raise ValueError when 'path' is converted to a non-existent Path
        """

        if not isinstance(path, (str, Path)):
            raise TypeError("Song.path must be a valid OS Path or a Path-convertible String!")
        else:
            path = Path(path).absolute().resolve()
            if path.exists() and path.is_absolute() and path.is_file():
                self._path = path
                return True
            else:
                raise ValueError("Song.path must be a valid OS Path to a file!")

    def set_title(self, title):
        """
        Sets a new title for the current Song object

        :param str title:

        :return True on success
        :rtype  Bool

        :raise TypeError when 'title' is not a String
        :raise ValueError when 'title' is an empty String
        """

        if not isinstance(title, str):
            raise TypeError("Song.title must be a valid String!")
        elif title == "":
            raise ValueError("Song.title cannot be an empty String!")
        else:
            self._title = title
            return True
