# VPH-002: Streaming Data với Dịch vụ AWS

## Mục tiêu
Triển khai dịch vụ **streaming data** sử dụng dịch vụ AWS:
- Amazon Kinesis Data Streams và Kinesis Firehose
- AWS Lambda

amazon/aws-lambda-python
saidsef/aws-kinesis-local

## Sử dụng eod_simulator
```python
venv➜ python3 services/eod_simulator/generate_postgres_data.py --n_sample 10
```