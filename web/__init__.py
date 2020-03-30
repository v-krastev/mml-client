from os import environ
from flask import Flask


def create_app():
    # create and configure the app:
    app = Flask(__name__, instance_relative_config=True)

    # Blueprint main_view:
    from .views import main_view
    from .backends.playback import Playback
    # init the backend used by Blueprint main_view :
    backend = Playback(songs_path=environ["MML_CLIENT_SONGS_PATH"],
                       pl_path=environ["MML_CLIENT_PLAYLISTS_PATH"])
    app.register_blueprint(main_view.bp, url_defaults={"backend": backend})

    return app
