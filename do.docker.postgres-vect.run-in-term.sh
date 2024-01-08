#!/usr/bin/bash

SCRIPT_NAME="$(/usr/bin/basename $0)"
SCRIPT_PATH="$(/usr/bin/dirname $0)"

DB_HOST=0.0.0.0
DB_PORT=5432

sudo docker run -p "$DB_HOST:$DB_PORT":5432 \
    -v "$SCRIPT_PATH/.DB_BOX":/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD="Gra.dum0k" \
    -e "TZ=Europe/Kiev" \
    --rm \
    -it \
    --name postgres-vect ankane/pgvector
