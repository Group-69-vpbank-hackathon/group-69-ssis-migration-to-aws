resource "aws_kinesis_stream" "data_stream" {
  name             = "${local.name_prefix}-data-stream"
  shard_count      = 2
  retention_period = 24

  shard_level_metrics = [
    "IncomingRecords",
    "OutgoingRecords",
  ]

  tags = local.common_tags
}

resource "aws_kinesis_firehose_delivery_stream" "backup_stream" {
  name        = "${local.name_prefix}-backup-firehose"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn           = aws_iam_role.firehose_role.arn
    bucket_arn         = aws_s3_bucket.backup_zone.arn
    prefix             = "year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/"
    error_output_prefix = "errors/"

    buffering_size         = 5
    buffering_interval     = 300
    compression_format  = "GZIP"
  }

  tags = local.common_tags
}
