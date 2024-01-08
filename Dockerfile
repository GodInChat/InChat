# Based on https://hub.docker.com/r/robd003/python3.10

FROM robd003/python3.10:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
# COPY alembic/ ./alembic/
# COPY alembic.ini ./
COPY main.py ./
COPY .env ./

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
CMD [ "uvicorn", "main:app", "--reload" ]
