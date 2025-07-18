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
    aws_glue_connection.vpc_network_config.name
  ]

  execution_property {
    max_concurrent_runs = 20
  }

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
    aws_glue_connection.vpc_network_config.name
  ]
  
  execution_property {
    max_concurrent_runs = 20
  }

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

  execution_property {
    max_concurrent_runs = 20
  }

  connections = [
    aws_glue_connection.vpc_network_config.name
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
    aws_glue_connection.vpc_network_config.name
  ]

  execution_property {
    max_concurrent_runs = 20
  }

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

  execution_property {
    max_concurrent_runs = 20
  }

  connections = [
    aws_glue_connection.vpc_network_config.name
  ]

  default_arguments = {
    "--extra-py-files" = "s3://${var.glue_bucket}/libs/libs.zip"
    "--TempDir"        = "s3://${var.glue_bucket}/glue_temp/"
    "--job-language"   = "python"
  }
}

resource "aws_glue_job" "etl_accomplisher" {
  name     = "etl_accomplisher_job"
  role_arn = aws_iam_role.glue_service_role.arn
  command {
    script_location = "s3://${var.glue_bucket}/glue_jobs/etl/run_etl_accomplisher.py"
    python_version  = "3"
  }
  max_capacity = 2
  glue_version = "3.0"

  connections = [
    aws_glue_connection.vpc_network_config.name
  ]

  execution_property {
    max_concurrent_runs = 20
  }
  
  default_arguments = {
    "--extra-py-files" = "s3://${var.glue_bucket}/libs/libs.zip"
    "--TempDir"        = "s3://${var.glue_bucket}/glue_temp/"
    "--job-language"   = "python"
  }
}

resource "aws_security_group" "glue_sg" {
  name        = "${var.project_name}-glue-sg"
  description = "Security group for Glue jobs running in VPC"
  vpc_id      = aws_vpc.main_vpc.id
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    self      = true
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-glue-sg"
  }
}
