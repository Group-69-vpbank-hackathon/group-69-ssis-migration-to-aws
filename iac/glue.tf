resource "aws_glue_connection" "vpc_network_config" {
  name            = "${var.project_name}-vpc-connection"
  connection_type = "NETWORK"
  physical_connection_requirements {
    subnet_id              = aws_subnet.private_subnet.id
    security_group_id_list = [aws_security_group.glue_sg.id]
    availability_zone      = aws_subnet.private_subnet.availability_zone
  }
}


resource "aws_glue_job" "csv_collector" {
  name     = "csv_collector_job"
  role_arn = aws_iam_role.glue_service_role.arn
  command {
    script_location = "s3://${var.glue_bucket}/glue_jobs/collectors/run_csv_collector.py"
    python_version  = "3"
  }
  max_capacity = 2
  glue_version = "3.0"

  connections = [
    aws_glue_connection.vpc_network_config.name,
    aws_glue_connection.postgres_jdbc_connection.name
  ]

  default_arguments = {
    "--extra-py-files" = "s3://${var.glue_bucket}/libs/libs.zip"
    "--TempDir"        = "s3://${var.glue_bucket}/glue_temp/"
    "--job-language"   = "python"
  }
}

resource "aws_glue_job" "postgres_collector" {
  name     = "postgres_collector_job"
  role_arn = aws_iam_role.glue_service_role.arn
  command {
    script_location = "s3://${var.glue_bucket}/glue_jobs/collectors/run_postgres_collector.py"
    python_version  = "3"
  }
  max_capacity = 2
  glue_version = "3.0"
  
  connections = [
    aws_glue_connection.vpc_network_config.name,
    aws_glue_connection.postgres_jdbc_connection.name
  ]
  
  default_arguments = {
    "--extra-py-files" = "s3://${var.glue_bucket}/libs/libs.zip"
    "--TempDir"        = "s3://${var.glue_bucket}/glue_temp/"
    "--job-language"   = "python"
  }
}

resource "aws_glue_job" "etl_loader" {
  name     = "etl_loader_job"
  role_arn = aws_iam_role.glue_service_role.arn
  command {
    script_location = "s3://${var.glue_bucket}/glue_jobs/etl/run_etl_loader.py"
    python_version  = "3"
  }
  max_capacity = 2
  glue_version = "3.0"

  connections = [
    aws_glue_connection.vpc_network_config.name,
    aws_glue_connection.postgres_jdbc_connection.name
  ]

  default_arguments = {
    "--extra-py-files" = "s3://${var.glue_bucket}/libs/libs.zip"
    "--TempDir"        = "s3://${var.glue_bucket}/glue_temp/"
    "--job-language"   = "python"
  }
}

resource "aws_glue_job" "etl_transformer" {
  name     = "etl_transformer_job"
  role_arn = aws_iam_role.glue_service_role.arn
  command {
    script_location = "s3://${var.glue_bucket}/glue_jobs/etl/run_etl_transformer.py"
    python_version  = "3"
  }
  max_capacity = 2
  glue_version = "3.0"

  connections = [
    aws_glue_connection.vpc_network_config.name,
    aws_glue_connection.postgres_jdbc_connection.name
  ]

  default_arguments = {
    "--extra-py-files" = "s3://${var.glue_bucket}/libs/libs.zip"
    "--TempDir"        = "s3://${var.glue_bucket}/glue_temp/"
    "--job-language"   = "python"
  }
}

resource "aws_glue_job" "etl_quality_checker" {
  name     = "etl_quality_checker_job"
  role_arn = aws_iam_role.glue_service_role.arn
  command {
    script_location = "s3://${var.glue_bucket}/glue_jobs/etl/run_etl_quality_checker.py"
    python_version  = "3"
  }
  max_capacity = 2
  glue_version = "3.0"

  connections = [
    aws_glue_connection.vpc_network_config.name,
    aws_glue_connection.postgres_jdbc_connection.name
  ]

  default_arguments = {
    "--extra-py-files" = "s3://${var.glue_bucket}/libs/libs.zip"
    "--TempDir"        = "s3://${var.glue_bucket}/glue_temp/"
    "--job-language"   = "python"
  }
}