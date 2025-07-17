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

        prefix             = "data/!{timestamp:yyyy-MM-dd'T'HH}UTC/"
        error_output_prefix = "errors/!{firehose:error-output-type}/!{timestamp:yyyy/MM/dd}UTC/"

        compression_format = "UNCOMPRESSED"
        buffering_interval = 60
        buffering_size     = 5

        processing_configuration {
            enabled = true
            processors {
                type = "Lambda"
                parameters {
                    parameter_name  = "LambdaArn"
                    parameter_value = aws_lambda_function.firehose_transformer.arn
                }
            }
        }
    }
}


resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.project_name}-lambda-firehose-transformer-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_exec_policy" {
  name = "${var.project_name}-lambda-firehose-transformer-policy"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # Cho phép ghi log ra CloudWatch Logs
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      },

      # Nếu Lambda cần ghi lại vào S3 (tùy thuộc vào logic bạn dùng)
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject"
        ],
        Resource = "${aws_s3_bucket.backup_streaming_zone_bucket.arn}/*"
      }
    ]
  })
}


resource "aws_lambda_function" "firehose_transformer" {
    function_name = "firehose-transformer"
    role          = aws_iam_role.lambda_exec_role.arn
    handler       = "firehose_transformer.lambda_function.lambda_handler"
    runtime       = "python3.12"
    timeout       = 10

    s3_bucket = "${var.lambda_artifacts_bucket}"
    s3_key    = "functions/firehose_transformer.zip"

    depends_on = [aws_s3_object.lambda_firehose_transformer]
}

resource "aws_lambda_permission" "allow_firehose_invoke" {
  statement_id  = "AllowExecutionFromFirehose"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.firehose_transformer.function_name
  principal     = "firehose.amazonaws.com"
  source_arn    = aws_kinesis_firehose_delivery_stream.firehose_to_s3.arn
}


