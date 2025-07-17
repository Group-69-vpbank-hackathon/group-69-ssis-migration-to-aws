resource "aws_secretsmanager_secret" "eod_creds" {
  name = "${var.project_name}-eod-credentials-v3"
}

resource "aws_secretsmanager_secret_version" "eod_creds_version" {
  secret_id = aws_secretsmanager_secret.eod_creds.id

  secret_string = jsonencode({
    username = var.postgres_username
    password = var.postgres_password
  })
}
