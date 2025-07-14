import os
import psycopg2
import base64
import json

PG_HOST = os.environ['PG_HOST']
PG_PORT = int(os.environ.get('PG_PORT', 5432))
PG_USER = os.environ['PG_USER']
PG_PASS = os.environ['PG_PASS']
PG_DB   = os.environ['PG_DB']

def lambda_handler(event, context):
    try:
        # Connect to Postgres
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            user=PG_USER,
            password=PG_PASS,
            dbname=PG_DB
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"PostgreSQL version: {version[0]}")
    except Exception as e:
        print("Error connecting to PostgreSQL:", str(e))
        return {"status": "error", "error": str(e)}

    for record in event['Records']:
        # Kinesis data is base64 encoded
        payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
        data = json.loads(payload)
        metadata = data["metadata"]
        data = data['data']
        if not data:
            continue
        
        print(f'----------------------- {metadata["table-name"]} -----------------------')
        print(data)

        # Build danh sách cột và giá trị, convert dict -> string nếu cần
        cols = list(data.keys())
        vals = [
            json.dumps(data[col], ensure_ascii=False) if isinstance(data[col], dict) else data[col]
            for col in cols
        ]

        table = metadata["table-name"]
        insert_cols = ', '.join([f'\"{col}\"' for col in cols])
        insert_vals = ', '.join(['%s'] * len(cols))

        insert_sql = f"""
            INSERT INTO \"{table}\" ({insert_cols})
            VALUES ({insert_vals});
        """
        print(insert_sql)

        cur.execute(insert_sql, vals)
        conn.commit()
        print("✅ insert success")
    cur.close()
    conn.close()

    return {"status": "ok"}

