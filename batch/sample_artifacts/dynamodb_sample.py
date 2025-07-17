#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3

# Initialize connections and faker
dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://dynamodb-local:8000",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)


def scan_sample_records(limit=10):
    table = dynamodb.Table("Transaction")
    response = table.scan(Limit=limit)

    print("\n===== SAMPLE RECORDS =====")
    for i, item in enumerate(response["Items"], 1):
        print(f"\nRecord #{i}:")
        for key, value in item.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")


if __name__ == "__main__":
    scan_sample_records()  # Thêm dòng này để xem 10 bản ghi mẫu
