resource "aws_s3_bucket" "backup_streaming_zone_bucket" {
  bucket = var.backup_streaming_zone_bucket

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

resource "aws_s3_bucket" "lambda_artifacts_bucket" {
  bucket = var.lambda_artifacts_bucket

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

resource "aws_s3_bucket" "streaming_failover_bucket" {
  bucket = var.streaming_failover_bucket

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

resource "aws_s3_bucket" "glue_bucket" {
  bucket = var.glue_bucket

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

resource "aws_s3_bucket" "landing_zone_bucket" {
  bucket = var.landing_zone_bucket

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

resource "aws_s3_bucket" "staging_zone_bucket" {
  bucket = var.staging_zone_bucket

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

resource "aws_s3_bucket" "silver_zone_bucket" {
  bucket = var.silver_zone_bucket

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}

resource "aws_s3_bucket" "gold_zone_bucket" {
  bucket = var.gold_zone_bucket

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Project   = var.project_name
    ManagedBy = "Terraform"
  }
}



# ============ copy file glue job to s3 =================
# Upload glue_jobs collectors
resource "aws_s3_object" "glue_collectors_run_csv" {
  bucket = "${var.glue_bucket}"
  key    = "glue_jobs/collectors/run_csv_collector.py"
  source = "${path.module}/../batch/glue_jobs/collectors/run_csv_collector.py"

  depends_on = [aws_s3_bucket.glue_bucket]
}

resource "aws_s3_object" "glue_collectors_run_postgres" {
  bucket = "${var.glue_bucket}"
  key    = "glue_jobs/collectors/run_postgres_collector.py"
  source = "${path.module}/../batch/glue_jobs/collectors/run_postgres_collector.py"

  depends_on = [aws_s3_bucket.glue_bucket]
}

# Upload glue_jobs etl
resource "aws_s3_object" "glue_etl_run_accomplisher" {
  bucket = "${var.glue_bucket}"
  key    = "glue_jobs/etl/run_etl_accomplisher.py"
  source = "${path.module}/../batch/glue_jobs/etl/run_etl_accomplisher.py"

  depends_on = [aws_s3_bucket.glue_bucket]
}

resource "aws_s3_object" "glue_etl_run_loader" {
  bucket = "${var.glue_bucket}"
  key    = "glue_jobs/etl/run_etl_loader.py"
  source = "${path.module}/../batch/glue_jobs/etl/run_etl_loader.py"

  depends_on = [aws_s3_bucket.glue_bucket]
}

resource "aws_s3_object" "glue_etl_run_quality_checker" {
  bucket = "${var.glue_bucket}"
  key    = "glue_jobs/etl/run_etl_quality_checker.py"
  source = "${path.module}/../batch/glue_jobs/etl/run_etl_quality_checker.py"

  depends_on = [aws_s3_bucket.glue_bucket]
}

resource "aws_s3_object" "glue_etl_run_transformer" {
  bucket = "${var.glue_bucket}"
  key    = "glue_jobs/etl/run_etl_transformer.py"
  source = "${path.module}/../batch/glue_jobs/etl/run_etl_transformer.py"

  depends_on = [aws_s3_bucket.glue_bucket]
}

# ==== upload scripts
resource "aws_s3_object" "glue_etl_script_cob_script" {
  bucket = "${var.glue_bucket}"
  key    = "glue_jobs/scripts/cob_script.sql"
  source = "${path.module}/../batch/etl/scripts/cob_script.sql"

  depends_on = [aws_s3_bucket.glue_bucket]
}

# ==== Upload libs.zip
resource "aws_s3_object" "libs_zip" {
  bucket = "${var.glue_bucket}"
  key    = "libs/libs.zip"
  source = "${path.module}/../batch/libs.zip"

  depends_on = [aws_s3_bucket.glue_bucket]
}

# ============ copy file lambda code to s3 =================
resource "aws_s3_object" "lambda_kinesis_consumer" {
  bucket = "${var.lambda_artifacts_bucket}"
  key    = "functions/kinesis_consumer.zip"
  source = "${path.module}/../streaming/lambda/kinesis_consumer.zip"

  depends_on = [aws_s3_bucket.lambda_artifacts_bucket]
}

resource "aws_s3_object" "lambda_dlq_handler" {
  bucket = "${var.lambda_artifacts_bucket}"
  key    = "functions/dlq_handler.zip"
  source = "${path.module}/../streaming/lambda/dlq_handler.zip"

  depends_on = [aws_s3_bucket.lambda_artifacts_bucket]
}

resource "aws_s3_object" "lambda_layer_psycopg2" {
  bucket = "${var.lambda_artifacts_bucket}"
  key    = "layers/psycopg2_layer.zip"
  source = "${path.module}/../streaming/lambda/psycopg2_layer.zip"

  depends_on = [aws_s3_bucket.lambda_artifacts_bucket]
}