# Description
Use the **mml-client** app to play music *(currently only `.mp3` files)* from a local or remote repo *(currently only `local`)* in your browser. Add your Songs, create new Playlists and assign them the Songs you want. When you are ready, press the Play button and **enjoy**.
>***NOTE*** The app is currently still ***in development***. This is a minimal working version, around which the rest of the features will be built.

# About
Why was this app created? Just playing-around with Python 3, web development, Docker, Jenkins, MySQL and frineds.<br>
Feel free to *Fork*, experiment and modify - it was created for ***learning purposes*** after all :).<br>
Any comments, questions or some other form of discussion/participation is welcomed!

---
---
---

# Content
- [Getting started](#getting-started)
  - [Instalation](#instalation)
  - [Usage](#usage)
- [Customization](#customization)
  - [CLI options](#cli-options)
  - [Environment variables](#environment-variables)
- [Notes on using the App with Docker](#notes-on-using-the-app-with-docker)
- [Notes on using the Jenkins container](#notes-on-using-the-jenkins-container)

<br>

## Getting started

### Instalation

    git clone https://github.com/v-krastev/mml_client.git
    cd mml_client

- Standalone:

      python -m venv venv
      source ./venv/bin/activate
      pip install -r requirements.txt

- with Docker:  
      
      ./run_mml-client_container.sh

> **OR**          
> Dockerfile and .dockerignore are included for a manual image build.
> The minimum requirements for the container to work as expected are:
> - -p {host_port}:5000   or  -P
> - --device /dev/snd   (this implying you actually need a working sound card on the host, to play any .mp3 files)


### Usage

- Standalone:
  - start with `python main.py`
  - exit with `Ctr+C` or `Ctr+D`
  
- with Docker:
  - start with `docker start mml-client` (it will be started immediately after installing it with `./run_mml-client_container.sh`)
  - exit with `docker stop mml-client` 

The App uses the default Flask port -> 5000<br>
<http://localhost:5000>

---
---

## Customization

The App currently supports couple of options to cusotmize its behaviour.<br>
They can be either passed as environment variables or as CLI options<br>

### CLI options

> --*option*=*VALUE*

The explicit passing of **CLI** options in the above format, when starting the App,<br>
will **take precedence** over any passed or previously existing **environment** variables!!!

<br>

#### -h | --help
  The default option of Python's *argparse* module.<br>
  Prints the available options and exits.
  - *Example usage*:  `python main.py -h`

<br>

#### --log-level
  Sets the log level for the entire App (***including*** for the Flask server)
  - default value: `info`
  - available values:
    - `debug`   | `DEBUG`
    - `info`    | `INFO`
    - `warning` | `WARNING`
    - `error`   | `ERROR`
    - `critical`| `CRITICAL`
  - *Example usage*:  `python main.py --log-level=debug`
  
<br>
  
#### --log-dir
  The local (from the App's perspective) directory, where the `.log` files will be saved.<br>
  The App will try to create the Path, if it's not existent on runtime.
  - default value: `./data/logs/`
  - available values: Any directory on the local filesystem, in which the user executing the app
  has permissions to create and modify files
  - *Example usage*:  `python main.py --log-dir=${HOME}/dir_will_be_created/and_this_one_too/`

<br>

#### --pl-dir
  The local directory, where the Playlist files will be saved.<br>
  The App will try to create the Path, if it's not existent on runtime.
  - default value: `./data/playlists/`
  - available values: Any directory on the local filesystem, in which the user executing the app
  has permissions to create and modify files
  - *Example usage*:  `python main.py --pl-dir=${HOME}/dir_will_be_created/and_this_one_too/`

<br>

#### --songs-dir
  The local directory, where the audio files (only `.mp3` for now) will be saved.<br>
  The App will try to create the Path, if it's not existent on runtime.
  - default value: `./data/songs/`
  - available values: Any directory on the local filesystem, in which the user executing the app
  has permissions to create and modify files
  - *Example usage*:  `python main.py --songs-dir=${HOME}/dir_will_be_created/and_this_one_too/`

<br>

#### --port
  The local port, on which the App can be accessed.<br>
  - default value: 5000
  - available values: any integer from 1025 to 65535 included (and not currently used)
  - *Example usage*: `python main.py --port=9090`

<br>
  
> With the current defaults for each option, plain run of the App (eg. only `python main.py`) is equivalent to:
> <pre>python main.py --log-level=info \
>                --log-dir=./data/logs \
>                --pl-dir=./data/playlists \
>		 --songs-dir=./data/songs \
>		 --port=5000 </pre>
  
<br>
<br>
  
### Environment variables
  
Currently, each [**CLI option**](#cli-options) has its **Environment variable** equivalent.<br>
Use them to set "new" defaults for the App, so `python main.py` with no `--option=VALUE` arguments<br>
would run with these predefined values. Probably more useful with the container.
>**NOTE** No matter if an **Environment variable** has been defined or not, if its `--option=VALUE` equivalent is present,
>the [**CLI option**](#cli-options) will take precedence.

<br>

#### MML_CLIENT_LOG_LEVEL
  - equivalent of the [--log-level](#--log-level) option
  
<br>
 
#### MML_CLIENT_LOG_DIR
  - equivalent of the [--log-dir](#--log-dir) option
  
<br>

#### MML_CLIENT_PLAYLISTS_PATH
  - equivalent of the [--pl-dir](#--pl-dir) option

<br>

#### MML_CLIENT_SONGS_PATH
  - equivalent of the [--songs-dir](#--songs-dir) option
  
<br>

#### FLASK_RUN_PORT
  - equivalent of the [--port](#--port) option
  
---
---

## Notes on using the App with Docker
>The `docker-compose.test.yml` file is used to Autobuild the image in the docker registry used in the Dockerfile

>Currently the App plays the audio files with the use of [ffmpeg](https://ffmpeg.org/) so it's installed in the image -> the extracted size is arround 550 MB and it takes some time to build it. That's why the `./run_in_docker.sh` script uses the uploaded [image](https://hub.docker.com/r/vkrastev/mml-client) in the docker.io registry, and not the included Dockerfile, as it's faster to just download instead of building from the ground-up.

>If you are not using the `./run_in_docker.sh` script to create the container, it's important to add the `--device=/dev/snd` directive, because, as stated above, the sound is played through the OS, not with the help of HTML (would probably change that in the future for obvious reasons)

>The `./run_in_docker.sh` script will create three named docker volumes mounted at the default locations for the [log](#--log-dir), the [songs](#--songs-dir) and the [playlists](#--pl-dir) folders. This gives some flexibility to spawn new containers with the previous data (ie. logs, songs, playlists) still being available for use.

>It doesn't make much sense to change the default locations for the data folders, without adjusting the mount points for the volumes - not only your previous data won't be available, any changes made in the new session (added songs, created playlists) will not be saved after the container is destroyed (unless for example you use the hacky way of committing the current state of the container to a new image and creating a new container from that image)

---
---

## Notes on using the Jenkins container
>Currently, only the creation of the container is implemented. On why such an aproach was taken (see the `make_docker_gid_equal()` function in the `run_jenkins_container.sh` script) - as the creator of the DinD concept himself [recommends](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/), for things like CI/CD, exposing the docker socket is the prefered way.

