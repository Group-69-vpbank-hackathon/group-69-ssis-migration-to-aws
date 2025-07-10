resource "aws_iam_role" "glue_service_role" {
  name = "glue_service_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "glue.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "glue_service_role_attach" {
  role       = aws_iam_role.glue_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_policy" "glue_s3_access" {
  name        = "glue_s3_access_policy"
  description = "Allow Glue to access S3 bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket",
        "s3:DeleteObject"
      ],
      Resource = [
        "arn:aws:s3:::${var.glue_bucket}",
        "arn:aws:s3:::${var.glue_bucket}/*",
        "arn:aws:s3:::${var.data_source_bucket}",
        "arn:aws:s3:::${var.data_source_bucket}/*",
        "arn:aws:s3:::${var.landing_zone_bucket}",
        "arn:aws:s3:::${var.landing_zone_bucket}/*",
        "arn:aws:s3:::${var.staging_zone_bucket}",
        "arn:aws:s3:::${var.staging_zone_bucket}/*",
        "arn:aws:s3:::${var.silver_zone_bucket}",
        "arn:aws:s3:::${var.silver_zone_bucket}/*",
        "arn:aws:s3:::${var.gold_zone_bucket}",
        "arn:aws:s3:::${var.gold_zone_bucket}/*",
      ]
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach_s3_policy" {
  role       = aws_iam_role.glue_service_role.name
  policy_arn = aws_iam_policy.glue_s3_access.arn
}

resource "aws_iam_policy" "glue_secretsmanager_access" {
  name        = "glue_secretsmanager_access_policy"
  description = "Allow Glue to get secrets"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret",
        "secretsmanager:ListSecrets"
      ],
      Resource = "*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach_secretsmanager_policy" {
  role       = aws_iam_role.glue_service_role.name
  policy_arn = aws_iam_policy.glue_secretsmanager_access.arn
}


resource "aws_iam_role" "sfn_exec_role" {
  name = "${var.project_name}-sfn-exec-role"

  # Cho phép dịch vụ Step Functions đảm nhận vai trò này
  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "states.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "sfn_glue_policy" {
  name   = "${var.project_name}-sfn-glue-policy"
  policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action = [
          "glue:StartJobRun",
          "glue:GetJobRun",
          "glue:GetJobRuns",
          "glue:BatchStopJobRun"
        ],
        # Cấp quyền trên tất cả các job đã tạo
        Resource = [
          aws_glue_job.csv_collector.arn,
          aws_glue_job.postgres_collector.arn,
          aws_glue_job.etl_loader.arn,
          aws_glue_job.etl_transformer.arn,
          aws_glue_job.etl_quality_checker.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sfn_glue_policy_attach" {
  role       = aws_iam_role.sfn_exec_role.name
  policy_arn = aws_iam_policy.sfn_glue_policy.arn
}