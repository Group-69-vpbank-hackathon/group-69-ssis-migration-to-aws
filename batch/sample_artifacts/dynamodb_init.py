#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
import time
import random
from faker import Faker
from decimal import Decimal
from multiprocessing import Pool, cpu_count
import argparse

# Initialize connections and faker
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://dynamodb-local:8000',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)
fake = Faker()

def ensure_transaction_table():
    # Kiểm tra và xoá bảng nếu đã tồn tại
    existing_tables = dynamodb.meta.client.list_tables()['TableNames']
    if 'Transaction' in existing_tables:
        print("Deleting existing table...")
        dynamodb.Table('Transaction').delete()
        # Đợi cho đến khi bảng được xoá hoàn toàn
        dynamodb.meta.client.get_waiter('table_not_exists').wait(
            TableName='Transaction'
        )
        print("Existing table deleted successfully!")

    # Tạo bảng mới
    print("Creating new table...")
    table = dynamodb.create_table(
        TableName='Transaction',
        KeySchema=[
            {'AttributeName': 'transaction_id', 'KeyType': 'HASH'},
            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'transaction_id', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'N'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    
    # Đợi cho đến khi bảng được tạo hoàn toàn
    table.wait_until_exists()
    print("New table created successfully!")
    return table

def generate_transaction(transaction_id):
    return {
        'transaction_id': transaction_id,
        'timestamp': int(time.time()),
        'customer_id': f"CUST-{random.randint(1000, 9999)}",
        'amount': Decimal(str(round(random.uniform(10.0, 1000.0), 2))),
        'merchant': fake.company(),
        'location': fake.city(),
        'payment_method': random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer']),
        'status': random.choice(['Completed', 'Pending', 'Failed']),
        'items': [
            {
                'product_id': f"PROD-{random.randint(100, 999)}",
                'quantity': random.randint(1, 5),
                'price': Decimal(str(round(random.uniform(5.0, 200.0), 2)))
            } for _ in range(random.randint(1, 3))
        ]
    }

def process_batch(batch_start_end):
    start, end = batch_start_end
    table = dynamodb.Table('Transaction')
    try:
        with table.batch_writer() as batch:
            for i in range(start, end):
                transaction = generate_transaction(f"TXN-{i:07d}")
                batch.put_item(Item=transaction)
        return (start, end, True)
    except Exception as e:
        return (start, end, False, str(e))

def insert_massive_data(total_records=1000000, batch_size=25000):
    table = ensure_transaction_table()
    start_time = time.time()
    
    num_batches = total_records // batch_size
    batches = [(i*batch_size, (i+1)*batch_size) for i in range(num_batches)]
    
    print(f"Starting to insert {total_records} records in batches of {batch_size}...")
    with Pool(processes=cpu_count()) as pool:
        results = pool.imap_unordered(process_batch, batches)
        
        for i, result in enumerate(results, 1):
            print(f"Processing batch {i}/{num_batches}...")
            if len(result) == 3:  # Success
                start, end, success = result
                elapsed = time.time() - start_time
                print(f"Completed batch {i}/{num_batches} ({start}-{end}) | Time: {elapsed:.2f}s")
            else:  # Error
                start, end, success, error = result
                print(f"Error in batch {i} ({start}-{end}): {error}")
    
    end_time = time.time()
    print(f"\nFinished inserting {total_records} records in {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=1000000)
    parser.add_argument('--batch', type=int, default=25000)
    args = parser.parse_args()
    
    insert_massive_data(total_records=args.count, batch_size=args.batch)