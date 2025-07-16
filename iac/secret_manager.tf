resource "aws_secretsmanager_secret" "postgres_creds" {
  name = "${var.project_name}-postgres-credentials"
}

resource "aws_secretsmanager_secret_version" "postgres_creds_version" {
  secret_id     = aws_secretsmanager_secret.postgres_creds.id

  secret_string = jsonencode({
    username = var.postgres_username
    password = var.postgres_password
  })
}

data "aws_secretsmanager_secret_version" "postgres_creds" {
  secret_id = aws_secretsmanager_secret.postgres_creds.id
}

