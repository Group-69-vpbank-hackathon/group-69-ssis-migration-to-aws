resource "aws_secretsmanager_secret" "eod_creds" {
  name = "${var.project_name}-eod-credentials-v6"
}

resource "aws_secretsmanager_secret_version" "eod_creds_version" {
  secret_id = aws_secretsmanager_secret.eod_creds.id

  secret_string = jsonencode({
    db_username = var.postgres_username
    db_password = var.postgres_password
  })
}
