# Based on https://hub.docker.com/r/robd003/python3.10
# Image robd003/python3.10 was
# `apt-get update && apt-get -y upgrade && apt-get autoremove`
# The result is python3.10_upd

FROM python3.10_upd:latest

WORKDIR /usr/src/app

RUN apt-get update && apt-get -y upgrade && apt-get autoremove

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY main.py ./
COPY .env ./
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY dbtest-sql.py ./
COPY dbtest-vec.py ./
COPY dbtest-noname-user.py ./
COPY main.sh ./

ENTRYPOINT [ "sh", "./main.sh" ]
