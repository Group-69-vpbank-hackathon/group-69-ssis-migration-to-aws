import json
import boto3
import os

s3 = boto3.client('s3')
BUCKET = os.environ['ARCHIVE_BUCKET']

def lambda_handler(event, context):
    print("📥 Incoming event:", event)

    # Lưu trữ các dòng JSONL
    lines = []

    for record in event['Records']:
        try:
            # Parse body JSON string thành list
            payload = json.loads(record['body'])  # 👈 Sửa: body là chuỗi JSON chứa list

            for item in payload:
                data = item.get("data")
                if data:
                    lines.append(json.dumps(data))  # 👈 Mỗi dòng là một JSON string

        except Exception as e:
            print(f"❌ Error parsing record: {e}")

    if not lines:
        print("⚠️ No valid data found.")
        return {"statusCode": 204}

    # Tạo tên file từ bản ghi đầu tiên
    first_item = json.loads(event['Records'][0]['body'])[0]
    table_name = first_item.get("table", "unknown_table")
    shard_seq = first_item.get("shardSequenceNumber", "shardId-000000000000:unknown")
    shard_id, seq_num = shard_seq.split(":")
    file_name = f"{table_name}/{shard_id}/seq-{seq_num}.jsonl"

    # Upload lên S3
    s3.put_object(
        Bucket=BUCKET,
        Key=file_name,
        Body="\n".join(lines).encode("utf-8"),
    )

    print(f"✅ Wrote {len(lines)} records to s3://{BUCKET}/{file_name}")
    return {"statusCode": 200}
