import os
import psycopg2


def get_pg_connection():
    conn = psycopg2.connect(
        host=os.environ["PG_HOST"],
        port=int(os.environ.get("PG_PORT", 5432)),
        user=os.environ["PG_USER"],
        password=os.environ["PG_PASS"],
        dbname=os.environ["PG_DB"],
    )
    cur = conn.cursor()
    return conn, cur
