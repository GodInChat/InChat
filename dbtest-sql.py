import psycopg2
from src.config import settings

POSTGRES_DB = settings.postgres_db
POSTGRES_USER = settings.postgres_user
POSTGRES_PASSWORD = settings.postgres_password
POSTGRES_PORT = settings.postgres_port
POSTGRES_HOST = settings.postgres_host

try:
    conn = psycopg2.connect(database=POSTGRES_DB,
                            user=POSTGRES_USER,
                            password=POSTGRES_PASSWORD,
                            host=POSTGRES_HOST, port=POSTGRES_PORT)
#except psycopg2.OperationalError as e:
except psycopg2.Error as e:
    # Here e.pgcode always is None, but str(e) can be:
    # connection to server at "127.0.0.1", port 5432 failed: FATAL:  database "inchat_sqldb2" does not exist
    # connection to server at "127.0.0.1", port 5432 failed: FATAL:  password authentication failed for user "postgres"
    # connection to server at "127.0.0.1", port 5433 failed: Connection refused
    #     Is the server running on that host and accepting TCP/IP connections?
    errmsg = str(e).lower()
    exitcode = 100
    if errmsg.find("does not exist") >= 0:
        exitcode = 100

        # Connection to database 'postgres'
        conn = psycopg2.connect(database="postgres",
                                user=POSTGRES_USER,
                                password=POSTGRES_PASSWORD,
                                host=POSTGRES_HOST, port=POSTGRES_PORT)
        try:
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE "{POSTGRES_DB}"')
            print(f"[OK] DATABASE {POSTGRES_DB} HAS BEEN CREATED SUCCESSFULLY: but need to run alembic upgrade");
            exit(exitcode)
        except psycopg2.Error as ee:
            print(f"Error {ee.pgcode}: Create database {POSTGRES_DB}: {str(ee)}", end="")
            exitcode=101

    elif errmsg.find("password authentication failed") >= 0:
        exitcode = 102
    elif errmsg.find("connection refused") >= 0:
        exitcode = 103
    print(f"Error {exitcode}: {str(e)}", end="")
    exit(exitcode)

print(f"[OK] DATABASE {POSTGRES_DB} ALREADY EXISTS")

# cursor = conn.cursor()
# cursor.execute('SELECT * FROM airport LIMIT 10')
# records = cursor.fetchall()
# cursor.close()

conn.close()
exit(0)
