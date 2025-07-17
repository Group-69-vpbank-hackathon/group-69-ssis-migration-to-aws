resource "aws_kinesis_firehose_delivery_stream" "firehose_to_s3" {
    name        = "${var.project_name}-firehose"
    destination = "extended_s3"

    kinesis_source_configuration {
        kinesis_stream_arn = aws_kinesis_stream.data_stream.arn
        role_arn           = aws_iam_role.firehose_role.arn
    }

    extended_s3_configuration {
        role_arn           = aws_iam_role.firehose_role.arn
        bucket_arn         = aws_s3_bucket.backup_streaming_zone_bucket.arn

        prefix             = "data/!{timestamp:yyyy-MM-dd'T'HH}'UTC'/"            # Ghi log bình thường
        error_output_prefix = "errors/!{firehose:error-output-type}/!{timestamp:yyyy/MM/dd}/"  # Ghi lỗi

        compression_format = "UNCOMPRESSED"
        buffering_interval = 60
        buffering_size     = 5
    }
}
