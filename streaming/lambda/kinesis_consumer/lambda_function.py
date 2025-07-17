import os
import json
import base64
from collections import defaultdict

from kinesis_consumer.utils.postgres import get_pg_connection
from kinesis_consumer.utils.sqs import send_batch_to_dlq

from kinesis_consumer.handler import TABLE_HANDLERS

DLQ_URL = os.environ["DLQ_URL"]


def lambda_handler(event, context):
    conn, cur = get_pg_connection()
    records_by_table = defaultdict(list)

    try:
        for record in event["Records"]:
            payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
            data = json.loads(payload)
            metadata = data.get("metadata", {})
            table = metadata.get("table-name")
            record_data = data.get("data")

            if not table or not record_data:
                print("❌ Missing table name or data")
                continue

            records_by_table[table].append((record_data, metadata))

        for table, records in records_by_table.items():
            handler = TABLE_HANDLERS.get(table, TABLE_HANDLERS["__default__"])
            handler(records, cur, conn)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error handling table {table}: {e}")
        cur.close()
        conn.close()

        send_batch_to_dlq(event["Records"], DLQ_URL)
        raise Exception("Some records failed, sent to DLQ.")

    return {"status": "ok"}
