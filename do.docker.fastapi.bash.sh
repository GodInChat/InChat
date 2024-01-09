#!/usr/bin/sh

docker="/usr/bin/docker"

sudo $docker run -it --rm --name inchat-fastapi --entrypoint=/bin/bash inchat-fastapi
