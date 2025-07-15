resource "aws_cloudwatch_log_group" "glue_logs" {
  name              = "/aws/glue/${local.name_prefix}"
  retention_in_days = 30
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${local.name_prefix}-glue-trigger"
  retention_in_days = 30
  tags = local.common_tags
} 