"""
    Connects the core scripts from bin/
    to provide a backend for main_view.py
"""


from bin import Crawler, Playlist, Song
from pathlib import Path
import logging

# for reading '.mp3' files:
from pydub import AudioSegment

# for playing '.mp3' files:
from simpleaudio import play_buffer, PlayObject


class Playback:
    def __init__(self, songs_path, pl_path, default_name="--all-songs--"):
        self.songs_path = songs_path    # set by Flask.app from an ENV variable
        self.pl_path = pl_path          # set by Flask.app from an ENV variable
        self._default_name = default_name

        # the default Playlist of all Song obj. in the repo:
        self.songs_in_repo = self._saved_songs_load()

        # list of all Playlist names in the repo:
        self.lists_in_repo = [self.songs_in_repo.name()] + self._saved_playlists_load()

        self.playlist = self.songs_in_repo
        self._song = PlayObject(play_id=1)

    def playlist_add(self, pl_name):
        """ Creates a new Playlist with the specified name
            Adds it to the Repo and saves it in the 'MML_CLIENT_PLAYLISTS_PATH' directory
            Returns the new (if created) or the current Playlist """

        # if a Playlist with the new name exists, do nothing:
        if pl_name is None or pl_name in self.lists_in_repo:
            return self.playlist

        tmp_pl = Playlist(pl_name)
        self.lists_in_repo.append(pl_name)
        tmp_pl.save(self.pl_path)

        # The Playlist constructor does NOT handle the possible PATH
        # of a file, where the Playlist obj. could be saved.
        # Only the save file is created by the Playlist.save() method
        # and NO Playlist.PATH modifications are made (it stays a '.').
        # Playlist.PATH is modified ONLY manually, or when the Playlist obj.
        # is LOADED with the Playlist.load() method !!!

        tmp_pl.path = Path(self.pl_path).joinpath(pl_name)
        return tmp_pl

    def playlist_change(self, pl_name):
        if pl_name == self.songs_in_repo.name():
            # switching to the already loaded default Playlist:
            return self.songs_in_repo
        else:
            # loading the new Playlist:
            tmp_path = Path(self.pl_path).joinpath(pl_name)
            return Playlist.load(tmp_path)

    def playlist_delete(self):
        # because 'Playlist.__eq__' compares the absolute Paths,
        # the default Playlist is in memory only (not in a file -> Path=='.')
        # checking if 'name' != 'default_name'
        if self.playlist.path is not None:
            del self.lists_in_repo[self.lists_in_repo.index(self.playlist.name())]
            Path.unlink(self.playlist.path)
            logging.info("Deleting MML-Playlist file: {}".format(self.playlist.path))
            self.playlist = self.songs_in_repo

    def _saved_playlists_load(self):
        # TODO use DB for this:
        """ Loading of created and saved Playlist NAMES!!!
            This is a temporary solution, should be read from a DB """
        playlist_names = []
        for playlist in Crawler.find_playlist(self.pl_path):
            playlist_names.append(str(playlist.name()))
        return playlist_names

    def _saved_songs_load(self):
        """ Creates the default Playlist
            with all of the '.mp3' files in 'MML_CLIENT_SONGS_PATH'
            This method is called only when the app starts
            and currently will NOT update if new files are added"""
        tmp_pl = Playlist(self._default_name)
        tmp_pl.add_songs(Crawler.find_songs(self.songs_path))
        return tmp_pl

    def song_add(self, audio_file):
        # !!! NOTE !!!: it makes more sense and would be quicker to
        # try loading the 'audio_file' as a Song object first
        # and only then save the file locally and add the Song
        # to the self.songs_in_repo Playlist, if the loading was successful.
        # However:
        # 1. If the App is being ran natively (no containers):
        #   - due to security, the object being sent from
        #     the browsers ('audio_file' in this case) contains
        #     a FAKE path, hiding where the file REALLY is on the disk
        #   - the Song.load() method works with an existing,
        #     absolute Path, pointing to a real file on the system,
        #     so no way to actually try loading the file, without
        #     knowing its real Path in the first place
        # 2. If the App is being ran in a container:
        #   - it has no way of connecting to the HOST's filesystem,
        #     except any bind mounts or volumes, so even only for a
        #     temporary work with a file, it has to be on the LOCAL filesystem

        # a local (from the App's perspective) path,
        # on successful save, the Song object will be loaded from here:
        new_song_path = Path(self.songs_path).joinpath(audio_file.filename)

        # duplicate the given FILE in the 'MML_CLIENT_SONGS_PATH' directory
        # this way, every run of the app will have access only
        # to it's locally saved Songs in 'MML_CLIENT_SONGS_PATH':
        audio_file.save(new_song_path)

        # create a new Song object from the audio file:
        tmp_song = Song.load(new_song_path)

        # if the audio file was actually parsed and can be played:
        if tmp_song is not None:
            # add the new Song to the repo:
            self.songs_in_repo.add_song(tmp_song)
        else:
            # the given file could not be parsed,
            # remove it from the local filesystem:
            Path.unlink(new_song_path)

    def song_is_playing(self):
        return self._song.is_playing()

    def song_play(self):
        if len(self.playlist) > 0:
            # the list is loaded, but nothing was played until now
            # "button_play pressed" and nothing selected:
            if self.playlist.current_song_index == -1:
                self.playlist.next_song()

            song_to_play = self.playlist.songs[self.playlist.current_song_index].path()

            try:
                sound = AudioSegment.from_mp3(song_to_play)
                self._song = play_buffer(sound.raw_data,
                                         num_channels=sound.channels,
                                         bytes_per_sample=sound.sample_width,
                                         sample_rate=sound.frame_rate)
                logging.info("Playing audio-file: {}".format(song_to_play))
            except Exception:
                logging.error("Could not open audio-file: {}".format(song_to_play))

    def song_stop(self):
        self._song.stop()
