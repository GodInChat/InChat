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
    cursor.execute("""INSERT INTO "user" (id, email, hashed_password, is_active, is_verified, is_superuser) """
                  +"""VALUES ('11111111-2222-3333-4444-555555555555', 'noname@google.com', """
                  +        """'$2b$12$00000000000000000000000000000000000000000000000000237', True, True, False)""")

    print("[OK] Absent user 'noname' is successfully inserted")

except psycopg2.Error as e:
    msg = str(e).lower()
    if msg.find("duplicate key") >= 0:
        print("[OK] User 'noname' already exists")
    else:
        print(f"Problem with 'noname' user: {str(e)}", end="")

cursor.close()
conn.close()
exit(0)
