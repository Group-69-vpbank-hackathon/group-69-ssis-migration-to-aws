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

# ===== Gán default glue service role cho Glue service role vừa tạo
resource "aws_iam_role_policy_attachment" "glue_service_role_attach" {
  role       = aws_iam_role.glue_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# ====== Tạo policy glue truy cập s3 =========
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
        "s3:DeleteObject",
        "s3:ListAllMyBuckets"
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

# ====== Policy glue truy cập secret manager =======
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

#===== tạo role cho step function
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

# === tạo policy step_function gọi glue job ========= 
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


#  ======= tạo IAM Role cho DMS truy cập Kinesis ==========
resource "aws_iam_role" "dms_kinesis_role" {
  name = "${var.project_name}-dms-kinesis-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "dms.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "dms_kinesis_policy" {
  role       = aws_iam_role.dms_kinesis_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonKinesisFullAccess"
}

# ======= IAM Role cho DMS truy cập Secrets Manager ===========
resource "aws_iam_role" "dms_secrets_role" {
  name = "${var.project_name}-dms-secrets-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "dms.amazonaws.com"
      }
    }]
  })
}

# ==== policy cho phép dms truy cập secret_manager để lấy credential
resource "aws_iam_role_policy_attachment" "dms_secrets_policy" {
  role       = aws_iam_role.dms_secrets_role.name
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}

## ======= Policy cho phép glue truy cập rds ===========
resource "aws_iam_policy" "glue_rds_access" {
  name        = "glue_rds_access_policy"
  description = "Allow Glue to access RDS Postgres"
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "rds-db:connect"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_rds_policy_attach" {
  role       = aws_iam_role.glue_service_role.name
  policy_arn = aws_iam_policy.glue_rds_access.arn
}


# ============ lambda full acess s3 ========

resource "aws_iam_role" "lambda_role" {
  name = "lambda-full-s3-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_s3_fullaccess" {
  name       = "lambda-s3-full-access"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}



# ======== lambda sqs ======

resource "aws_iam_role" "lambda_sqs_producer_role" {
  name = "lambda-producer-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_sqs_producer_policy" {
  name = "lambda-producer-sqs-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "kinesis:GetRecords",
          "kinesis:GetShardIterator",
          "kinesis:DescribeStream",
          "kinesis:ListStreams"
        ]
        Resource = aws_kinesis_stream.data_stream.arn 
      },
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage"
        ]
        Resource = aws_sqs_queue.dlq_queue_records.arn
      },
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage"
        ]
        Resource = aws_sqs_queue.dlq_queue_metadata.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_producer_attach" {
  role       = aws_iam_role.lambda_sqs_producer_role.name
  policy_arn = aws_iam_policy.lambda_sqs_producer_policy.arn
}


resource "aws_iam_role" "lambda_sqs_consumer_role" {
  name = "lambda-consumer-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_sqs_consumer_policy" {
  name = "lambda-consumer-sqs-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = aws_sqs_queue.dlq_queue_records.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_consumer_attach" {
  role       = aws_iam_role.lambda_sqs_consumer_role.name
  policy_arn = aws_iam_policy.lambda_sqs_consumer_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_consumer_attach_s3" {
  role       = aws_iam_role.lambda_sqs_consumer_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}


resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.lambda_sqs_producer_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access_dlq" {
  role       = aws_iam_role.lambda_sqs_consumer_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}


# ===== firehose 

resource "aws_iam_role" "firehose_role" {
  name = "${var.project_name}-firehose-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "firehose.amazonaws.com"
      }
    }]
  })
}


resource "aws_iam_role_policy" "firehose_policy" {
  name = "${var.project_name}-firehose-policy"
  role = aws_iam_role.firehose_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
            "s3:PutObject",
            "s3:PutObjectAcl",
            "s3:GetObject",
            "s3:ListBucket"
        ],
        Resource = "${aws_s3_bucket.backup_streaming_zone_bucket.arn}/*"
      },
      {
        Effect = "Allow",
        Action = [
          "kinesis:DescribeStream",
          "kinesis:GetShardIterator",
          "kinesis:GetRecords",
          "kinesis:ListShards"
        ],
        Resource = aws_kinesis_stream.data_stream.arn
      },
      {
        Effect = "Allow",
        Action = "lambda:InvokeFunction",
        Resource = aws_lambda_function.firehose_transformer.arn
      },

      {
        Effect = "Allow",
        Action = [
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
}

