import argparse
import logging
from os import environ, path, makedirs
import web


def init_logging(level, log_dir):
    log_file = path.join(log_dir, "mml_main.log")
    if level == logging.DEBUG:
        logging.basicConfig(filename=log_file,
                            filemode='a',
                            style='{',
                            format="\n[{asctime}] {levelname}: {message}\n"
                                   "Module: {module}\n"
                                   "Method: {funcName}",
                            datefmt="%d.%m.%Y %H:%M:%S",
                            level=logging.DEBUG)
        logging.info("Starting MML_CLIENT in DEBUG mode...")
    else:
        logging.basicConfig(filename=log_file,
                            filemode='a',
                            style='{',
                            format="[{asctime}] {levelname}: {message}",
                            datefmt="%d.%m.%Y %H:%M:%S",
                            level=level)
        logging.info("Starting MML_CLIENT...")
    pass


def set_vars():
    parser = argparse.ArgumentParser()

    logging_options = parser.add_argument_group(title="MML-Client Logging options")
    logging_options.add_argument("--log-level",
                                 required=False,
                                 type=str,
                                 choices=["debug", "DEBUG",
                                          "info", "INFO",
                                          "warning", "WARNING",
                                          "error", "ERROR",
                                          "critical", "CRITICAL"],
                                 metavar="LEVEL",
                                 help="Logging level")
    logging_options.add_argument("--log-dir",
                                 required=False,
                                 type=str,
                                 metavar="DIR",
                                 help="Directory to store the logs")

    path_options = parser.add_argument_group(title="MML-Client path options")
    path_options.add_argument("--pl-dir",
                              required=False,
                              type=str,
                              metavar="DIR",
                              help="Directory of saved Playlist files to use")
    path_options.add_argument("--songs-dir",
                              required=False,
                              type=str,
                              metavar="DIR",
                              help="Directory of saved audio files to use")

    web_server_options = parser.add_argument_group(title="MML-Client web server options")
    web_server_options.add_argument("--port",
                                    required=False,
                                    type=int,
                                    choices=iter(range(1025, 65536)),
                                    metavar="PORT",
                                    help="The local port from which to access the App")

    args = parser.parse_args()

    if args.log_level:
        # if set by the CLI:
        log_level = args.log_level.lower()
    else:
        # if not set by the CLI, use the ENV:
        log_level = environ.get("MML_CLIENT_LOG_LEVEL", default="info")
    # export to the ENV:
    environ["MML_CLIENT_LOG_LEVEL"] = log_level

    if args.log_dir:
        # if set by the CLI:
        log_dir = args.log_dir
    else:
        # if not set by the CLI, use the ENV:
        log_dir = environ.get("MML_CLIENT_LOG_DIR", default="./data/logs/")
    # if necessary, create the directory:
    makedirs(log_dir, exist_ok=True)
    # export to the ENV:
    environ["MML_CLIENT_LOG_DIR"] = log_dir

    if args.pl_dir:
        # if set by the CLI:
        pl_dir = args.pl_dir
    else:
        # if not set by the CLI, use the ENV:
        pl_dir = environ.get("MML_CLIENT_PLAYLISTS_PATH", default="./data/playlists/")
    # if necessary, create the directory:
    makedirs(pl_dir, exist_ok=True)
    # export to the ENV:
    environ["MML_CLIENT_PLAYLISTS_PATH"] = pl_dir

    if args.songs_dir:
        # if set by the CLI:
        songs_dir = args.songs_dir
    else:
        # if not set by the CLI, use the ENV:
        songs_dir = environ.get("MML_CLIENT_SONGS_PATH", default="./data/songs/")
    # if necessary, create the directory:
    makedirs(songs_dir, exist_ok=True)
    # export to the ENV:
    environ["MML_CLIENT_SONGS_PATH"] = songs_dir

    if args.port:
        # export the ENV:
        environ["FLASK_RUN_PORT"] = str(args.port)
    else:
        # export the ENV:
        environ["FLASK_RUN_PORT"] = "5000"


if __name__ == "__main__":
    # if '-h' or '--help' is passed, the script exits:
    set_vars()

    # work with 'logging' inner numeric values:
    log_level = getattr(logging, environ["MML_CLIENT_LOG_LEVEL"].upper(), None)
    init_logging(level=log_level, log_dir=environ["MML_CLIENT_LOG_DIR"])
    logger = logging.getLogger(__name__)

    # init the Web-Server:
    app = web.create_app()

    # set the Web-Server's log-level:
    if environ["MML_CLIENT_LOG_LEVEL"].lower() == "debug":
        debug_server = True
    else:
        debug_server = False

    # TODO: host="0.0.0.0" is required by Docker
    # start the Web-Server:
    app.run(debug=debug_server, host="0.0.0.0", port=environ["FLASK_RUN_PORT"])
