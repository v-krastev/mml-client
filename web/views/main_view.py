import logging
from os import environ
from flask import Blueprint, render_template, request, redirect, url_for


bp = Blueprint("main_view", __name__)


@bp.route("/", methods=["GET", "POST"])
def main_screen(backend):
    logging.debug("Server path: {}  Method: {}".format(request.path, request.method))
    return render_template("main_view/index.html",
                           all_playlists=backend.lists_in_repo,
                           all_songs=backend.songs_in_repo,
                           current_playlist=backend.playlist,
                           song_playing=False)


@bp.route("/create_playlist", methods=["POST"])
def create_playlist(backend):
    logging.debug("Server path: {}  Method: {}".format(request.path, request.method))
    if request.form.get("new_pl_name") != "" and request.form.get("new_pl_name") != backend.lists_in_repo[0]:
        # create the new Playlist and assign as the current_playlist:
        backend.playlist = backend.playlist_add(request.form.get("new_pl_name"))
        backend.song_stop()
    return redirect(url_for("main_view.main_screen"))


@bp.route("/load_playlist", methods=["POST"])
def load_playlist(backend):
    logging.debug("Server path: {}  Method: {}".format(request.path, request.method))
    backend.song_stop()
    backend.playlist = backend.playlist_change(request.form.get("playlists"))
    return redirect(url_for("main_view.main_screen"))


@bp.route("/delete_playlist", methods=["POST"])
def delete_playlist(backend):
    logging.debug("Server path: {}  Method: {}".format(request.path, request.method))
    backend.playlist_delete()
    return redirect(url_for("main_view.main_screen"))


@bp.route("/add_song", methods=["POST"])
def add_song(backend):
    logging.debug("Server path: {}  Method: {}".format(request.path, request.method))
    # no Song selected to be added:
    if request.form["add_songs"] == "Select":
        return redirect(url_for("main_view.play_song"))
    else:
        song_index = int(request.form["add_songs"])
        backend.playlist.add_song(backend.songs_in_repo.songs[song_index])
        backend.playlist.save(environ["MML_CLIENT_PLAYLISTS_PATH"])
        return redirect(url_for("main_view.play_song"))


@bp.route("/add_file", methods=["POST"])
def add_file(backend):
    audio_files = request.files["audio_files"]
    backend.song_add(audio_files)
    return redirect(url_for("main_view.play_song"))


@bp.route('/playing', methods=["GET", "POST"])
def play_song(backend):
    # only the buttons controlling the audio are doing something
    # any redirects TO the page are just refreshing it with the different content

    logging.debug("Server path: {}  Method: {}".format(request.path, request.method))
    if request.method == "POST":
        if "button_prev" in request.form:
            if backend.playlist.current_song_index != backend.playlist.prev_song():
                if backend.song_is_playing():
                    backend.song_stop()
                    backend.song_play()
        elif "button_play" in request.form:
            # if song_is_playing, button_PLAY is button_STOP:
            if backend.song_is_playing():
                backend.song_stop()
                return redirect(url_for("main_view.main_screen"))
            else:
                backend.song_play()
                # when the list is empty:
                if not backend.song_is_playing():
                    return redirect(url_for("main_view.main_screen"))
        elif "button_next" in request.form:
            if backend.playlist.current_song_index != backend.playlist.next_song():
                if backend.song_is_playing():
                    backend.song_stop()
                    backend.song_play()
    elif request.method == "GET":
        # manually entered path or refreshing while song is stopped
        if not backend.song_is_playing():
            return redirect(url_for("main_view.main_screen"))
    return render_template("main_view/index.html",
                           all_playlists=backend.lists_in_repo,
                           all_songs=backend.songs_in_repo,
                           current_playlist=backend.playlist,
                           song_playing=backend.song_is_playing())


@bp.route('/options', methods=["POST"])
def song_options(backend):
    logging.debug("Server path: {}  Method: {}".format(request.path, request.method))
    if "button_up" in request.form:
        backend.playlist.swap_songs(backend.playlist.current_song_index, backend.playlist.prev_song())
    elif "button_down" in request.form:
        backend.playlist.swap_songs(backend.playlist.current_song_index, backend.playlist.next_song())
    elif "button_remove" in request.form:
        backend.song_stop()
        backend.playlist.remove_song(backend.playlist.current_song_index)

    # avoid modifying the default Playlist:
    if backend.playlist.name() != backend.songs_in_repo.name():
        backend.playlist.save(environ["MML_CLIENT_PLAYLISTS_PATH"])
    return redirect(url_for("main_view.play_song"))
