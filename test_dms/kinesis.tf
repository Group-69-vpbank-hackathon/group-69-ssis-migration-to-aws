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

 output "data_stream_arn" {
       value = aws_kinesis_stream.data_stream.arn
     }