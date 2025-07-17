import boto3
import json
import base64
from collections import defaultdict
from botocore.config import Config

MAX_SQS_MESSAGE_SIZE = 200 * 1024
sqs_client = boto3.client(
    "sqs",
    config=Config(retries={"max_attempts": 3, "mode": "standard"})
)
def send_batch_to_dlq(records_list, dlq_url):
    records_by_table = defaultdict(list)

    try:
        for record in records_list:
            payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
            data = json.loads(payload)
            
            metadata = data.get("metadata", {})
            shard_sequence_number = record["eventID"]
            table = metadata.get("table-name")
            record_data = data.get("data")

            if not table or not record_data:
                print("❌ Missing table name or data")
                continue

            records_by_table[table].append({
                "table": table,
                "shardSequenceNumber": shard_sequence_number,
                "metadata": metadata,
                "data": record_data
            })

        for table, records in records_by_table.items():
            print(f"Preparing to send {len(records)} records for table '{table}' to DLQ")

            current_batch = []
            current_size = 0

            for r in records:
                body = json.dumps(r, ensure_ascii=False)
                body_size = len(body.encode("utf-8"))

                if current_size + body_size > MAX_SQS_MESSAGE_SIZE:
                    sqs_client.send_message(
                        QueueUrl=dlq_url,
                        MessageBody=json.dumps(current_batch, ensure_ascii=False)
                    )
                    print(f"✅ Sent batch with {len(current_batch)} records for table '{table}'")

                    current_batch = []
                    current_size = 0

                current_batch.append(r)
                current_size += body_size

            if current_batch:
                sqs_client.send_message(
                    QueueUrl=dlq_url,
                    MessageBody=json.dumps(current_batch, ensure_ascii=False)
                )
                print(f"✅ Sent final batch with {len(current_batch)} records for table '{table}'")

    except Exception as e:
        print(f"❌ Error sending batch to DLQ: {e}")
        raise Exception("Failed to send batch to DLQ.")

    