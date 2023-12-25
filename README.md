# InChat

## Base project set up

1. ensure your postgres and redis instances are running
2. install virtual environment with poetry
3. copy example.env file th the same directory, rename into .env
4. edit credentials in .env file
5. run command 'poetry install'
6. run command 'alembic upgrade head'. it will install all necessary tables into database.
7. run command 'uvicorn main:app'

note: emailing is disabled. Just put some placeholders into .env
