#############################################
# S3 BUCKETS
#############################################

resource "aws_s3_bucket" "data_lake" {
  bucket = "${local.name_prefix}-data-lake"
  tags   = local.common_tags
}

resource "aws_s3_bucket" "backup_zone" {
  bucket = "${local.name_prefix}-backup-zone"
  tags   = local.common_tags
}

resource "aws_s3_bucket" "processed_zone" {
  bucket = "${local.name_prefix}-processed-zone"
  tags   = local.common_tags
}

#############################################
# VERSIONING
#############################################

resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "backup_zone_versioning" {
  bucket = aws_s3_bucket.backup_zone.id

  versioning_configuration {
    status = "Enabled"
  }
}

#############################################
# SERVER-SIDE ENCRYPTION
#############################################

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake_encryption" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backup_zone_encryption" {
  bucket = aws_s3_bucket.backup_zone.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

#############################################
# S3 → Lambda NOTIFICATION
#############################################

resource "aws_lambda_permission" "s3_invoke_lambda" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.glue_trigger.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.backup_zone.arn
}


resource "aws_s3_bucket_notification" "backup_notification" {
  bucket = aws_s3_bucket.backup_zone.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.glue_trigger.arn
    events              = ["s3:ObjectCreated:*"]
    # filter_prefix     = "data/" # Optional: uncomment if you only want to trigger for specific prefixes
  }

  depends_on = [aws_lambda_permission.s3_invoke_lambda]
}

resource "aws_s3_bucket" "codepipeline_artifacts" {
  bucket = "${local.name_prefix}-codepipeline-artifacts"
  tags   = local.common_tags
}
