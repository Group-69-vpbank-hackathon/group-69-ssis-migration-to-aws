resource "aws_lambda_function" "kinesis_consumer" {
    role          = aws_iam_role.lambda_sqs_producer_role.arn
    function_name = "kinesis_consumer"
    handler       = "kinesis_consumer.lambda_function.lambda_handler"
    runtime       = "python3.12"
    layers        = [aws_lambda_layer_version.psycopg2_layer.arn]

    s3_bucket = "${var.lambda_artifacts_bucket}"
    s3_key    = "functions/kinesis_consumer.zip"

    environment {
      variables = {
        DLQ_URL = aws_sqs_queue.dlq_queue_records.url
        PG_HOST = aws_db_instance.db_app.address
        PG_PORT = "5432"
        PG_USER = var.postgres_username
        PG_PASS = var.postgres_password
        PG_DB   = var.postgres_db_name
      }
    }

    timeout = 600
    vpc_config {
      subnet_ids         = [
        aws_subnet.private_subnet_a.id,
        aws_subnet.private_subnet_b.id
      ]
      security_group_ids = [aws_security_group.lambda_sg.id]
    }
}

resource "aws_lambda_layer_version" "psycopg2_layer" {
  layer_name             = "psycopg2"
  compatible_runtimes    = ["python3.12"]
  compatible_architectures = ["x86_64"]

  s3_bucket = "${var.lambda_artifacts_bucket}"
  s3_key    = "layers/psycopg2_layer.zip"
}

resource "aws_lambda_function" "dlq_handler" {
    role          = aws_iam_role.lambda_sqs_consumer_role.arn
    function_name = "dlq_handler"
    handler       = "dlq_handler.dlq_handler.lambda_handler"
    runtime       = "python3.12"

    s3_bucket = "${var.lambda_artifacts_bucket}"
    s3_key    = "functions/dlq_handler.zip"

    timeout = 600

    vpc_config {
      subnet_ids         = [
        aws_subnet.private_subnet_a.id,
        aws_subnet.private_subnet_b.id
      ]
      security_group_ids = [aws_security_group.lambda_sg.id]
    }

    environment {
      variables = {
        ARCHIVE_BUCKET = var.streaming_failover_bucket
      }
    }
}

# ====== config để gắn Kinesis trigger
resource "aws_lambda_event_source_mapping" "kinesis_consumer_trigger" {
  event_source_arn  = aws_kinesis_stream.data_stream.arn
  function_name     = aws_lambda_function.kinesis_consumer.arn
  starting_position = "LATEST"

  batch_size = 10
  maximum_batching_window_in_seconds = 10

  enabled = true
  maximum_retry_attempts = 1

  destination_config {
    on_failure {
      destination_arn = aws_sqs_queue.dlq_queue_metadata.arn
    }
  }

  bisect_batch_on_function_error = false

  maximum_record_age_in_seconds = -1
}

#======== config để dlq_handler lambda xử lí SQS dlq =====
resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn  = aws_sqs_queue.dlq_queue_records.arn
  function_name     = aws_lambda_function.dlq_handler.arn
  enabled           = true

  batch_size                         = 10
  maximum_batching_window_in_seconds = 30

  function_response_types = ["ReportBatchItemFailures"]
}
resource "aws_security_group" "lambda_sg" {
  name        = "lambda-sg"
  description = "Allow Lambda outbound HTTPS to VPC Endpoints"
  vpc_id      = aws_vpc.main_vpc.id

  egress {
    description = "Allow HTTPS to anywhere (NAT or VPC Endpoints)"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}