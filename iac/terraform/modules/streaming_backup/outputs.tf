output "bucket_arn" {
  value = aws_s3_bucket.backup.arn
}

output "firehose_arn" {
  value = aws_kinesis_firehose_delivery_stream.firehose.arn
}
