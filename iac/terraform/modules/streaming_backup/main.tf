resource "aws_s3_bucket" "backup" {
  bucket = var.bucket_name
  force_destroy = true
}

resource "aws_iam_role" "firehose_delivery_role" {
  name = "firehose_delivery_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "firehose.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "firehose_policy" {
  name = "firehose_policy"
  role = aws_iam_role.firehose_delivery_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:AbortMultipartUpload",
          "s3:GetBucketLocation",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:ListBucketMultipartUploads",
          "s3:PutObject"
        ]
        Resource = [
          aws_s3_bucket.backup.arn,
          "${aws_s3_bucket.backup.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "kinesis:DescribeStream",
          "kinesis:GetShardIterator",
          "kinesis:GetRecords",
          "kinesis:ListShards"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_kinesis_stream" "this" {
  name             = var.stream_name
  shard_count      = 1
  retention_period = 24
}

resource "aws_kinesis_firehose_delivery_stream" "firehose" {
  name        = var.firehose_name
  destination = "s3"

  kinesis_source_configuration {
    kinesis_stream_arn = aws_kinesis_stream.this.arn
    role_arn           = aws_iam_role.firehose_delivery_role.arn
  }

  s3_configuration {
    role_arn           = aws_iam_role.firehose_delivery_role.arn
    bucket_arn         = aws_s3_bucket.backup.arn

    prefix             = "firehose/!{timestamp:yyyy-MM-dd'T'HH}/"
    error_output_prefix = "firehose-error/!{firehose:error-output-type}/!{timestamp:yyyy-MM-dd}/"
    buffering_size     = 1
    buffering_interval = 60
    compression_format = "UNCOMPRESSED"
  }
}
