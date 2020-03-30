#! /bin/bash

docker container run \
	-d \
	--name mml-client \
	-p 5000:5000 \
	--mount type=volume,source=mml-client_logs,target=/app/data/logs \
	--mount type=volume,source=mml-client_playlists,target=/app/data/playlists \
	--mount type=volume,source=mml-client_songs,target=/app/data/songs \
	--device /dev/snd \
	vkrastev/mml-client:latest
