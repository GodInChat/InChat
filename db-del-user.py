# Check existence of the mandatory "nonam"e user.

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

    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM "user" WHERE email = 'akashyren77@gmail.com'""")

    print("[OK] User is successfully deleted")

except psycopg2.Error as e:
    msg = str(e).lower()
    print(f"[ERR] {str(e)}", end="")

cursor.close()
conn.close()
exit(0)
