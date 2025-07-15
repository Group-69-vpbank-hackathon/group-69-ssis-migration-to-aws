

resource "aws_lambda_function" "kinesis_to_onprem" {
  function_name = "${local.name_prefix}-kinesis-to-onprem"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.11"
  handler       = "main.lambda_handler"
  timeout       = 300

  filename         = "${path.module}/lambda/kinesis_to_onprem.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/kinesis_to_onprem.zip")

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = {
      DB_SECRET_ARN = aws_secretsmanager_secret.db_credentials.arn
    }
  }

  tags = local.common_tags
}

resource "aws_lambda_event_source_mapping" "from_kinesis" {
  event_source_arn  = aws_kinesis_stream.data_stream.arn
  function_name     = aws_lambda_function.kinesis_to_onprem.arn
  starting_position = "LATEST"
  batch_size        = 100
  enabled           = true
}

resource "aws_lambda_function" "glue_trigger" {
  function_name = "${local.name_prefix}-glue-trigger"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.11"
  handler       = "main.lambda_handler"
  filename         = "${path.module}/lambda/glue_trigger.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda/glue_trigger.zip")
  tags             = local.common_tags
}
