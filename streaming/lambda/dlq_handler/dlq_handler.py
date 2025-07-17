import json
import boto3
import os
from datetime import datetime
import uuid

s3 = boto3.client('s3')
BUCKET = os.environ['ARCHIVE_BUCKET']

def lambda_handler(event, context):
    now = datetime.utcnow()
    timestamp_str = now.strftime("%Y-%m-%dT%H-%M-%S")
    random_suffix = uuid.uuid4().hex[:6]

    file_name = f"archive/{timestamp_str}-{random_suffix}.jsonl"

    lines = []
    for record in event["Records"]:
        try:
            body = record['body']
            lines.append(body)
        except Exception as e:
            print(f"❌ Error parsing record: {e}")

    # Ghi tất cả records vào 1 file JSON Lines
    s3.put_object(
        Bucket=BUCKET,
        Key=file_name,
        Body="\n".join(lines).encode("utf-8")
    )

    print(f"✅ Wrote {len(lines)} records to {file_name}")
    return {"statusCode": 200}
