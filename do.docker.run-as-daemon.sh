#!/usr/bin/sh

docker="/usr/bin/docker"

sudo $docker run -d --rm --network="host" \
    -e OLLAMA_URL=http://172.27.72.6:11434 \
    --name inchat-fastapi inchat-fastapi
