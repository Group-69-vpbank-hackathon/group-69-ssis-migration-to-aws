  ##############################
  # Subnet Group cho DMS
  ##############################
  resource "aws_dms_replication_subnet_group" "dms_subnet_group" {
    replication_subnet_group_id          = "${local.name_prefix}-dms-subnet-group"
    replication_subnet_group_description = "DMS subnet group for ${local.name_prefix}"
    subnet_ids                          = [aws_subnet.private[0].id, aws_subnet.private[1].id]
    tags                                = local.common_tags
  }

  ##############################
  # IAM Role cho DMS → Kinesis
  ##############################
  resource "aws_iam_role" "dms_kinesis_role" {
    name = "${local.name_prefix}-dms-kinesis-role"
    assume_role_policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Effect = "Allow",
          Principal = {
            Service = "dms.amazonaws.com"
          },
          Action = "sts:AssumeRole"
        }
      ]
    })

    tags = local.common_tags
  }

  resource "aws_iam_policy" "dms_kinesis_policy" {
    name = "${local.name_prefix}-dms-kinesis-policy"
    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Effect = "Allow",
          Action = [
            "kinesis:DescribeStream",
            "kinesis:PutRecord",
            "kinesis:PutRecords"
          ],
          Resource = aws_kinesis_stream.data_stream.arn
        }
      ]
    })
  }

  resource "aws_iam_role_policy_attachment" "dms_kinesis_attach" {
    role       = aws_iam_role.dms_kinesis_role.name
    policy_arn = aws_iam_policy.dms_kinesis_policy.arn
  }

  ##############################
  # DMS Replication Instance
  ##############################
  resource "aws_dms_replication_instance" "dms_instance" {
    replication_instance_id      = "${local.name_prefix}-dms-instance"
    replication_instance_class   = "dms.t3.medium"
    allocated_storage            = 20
    apply_immediately            = true
    auto_minor_version_upgrade   = true
    engine_version               = "3.5.4"
    # availability_zone            = "us-east-1a"
    multi_az                     = true
    publicly_accessible          = false
    replication_subnet_group_id  = aws_dms_replication_subnet_group.dms_subnet_group.id
    vpc_security_group_ids       = [aws_security_group.dms_sg.id]

    tags = local.common_tags
  }

  ##############################
  # DMS Source Endpoint (PostgreSQL - Supabase)
  ##############################
  resource "aws_dms_endpoint" "source" {
    endpoint_id   = "${local.name_prefix}-supabase-source"
    endpoint_type = "source"
    engine_name   = "postgres"
    server_name   = var.source_database_endpoint
    port          = var.db_port
    database_name = var.db_name
    username      = var.db_username
    password      = var.db_password
    ssl_mode      = "require" # Supabase thường yêu cầu SSL

    tags = local.common_tags
  }

  ##############################
  # DMS Target Endpoint (Kinesis)
  ##############################
  resource "aws_dms_endpoint" "kinesis_target" {
    endpoint_id   = "${local.name_prefix}-kinesis-target"
    endpoint_type = "target"
    engine_name   = "kinesis"

    kinesis_settings {
      stream_arn              = aws_kinesis_stream.data_stream.arn
      message_format          = "json"
      service_access_role_arn = aws_iam_role.dms_kinesis_role.arn
    }

    ssl_mode = "none"

    tags = local.common_tags
  }

  ##############################
  # DMS Replication Task (CDC)
  ##############################
  resource "aws_dms_replication_task" "cdc_to_kinesis" {
    replication_task_id           = "${local.name_prefix}-cdc-to-kinesis"
    migration_type                = "cdc"
    replication_instance_arn      = aws_dms_replication_instance.dms_instance.replication_instance_arn
    source_endpoint_arn           = aws_dms_endpoint.source.endpoint_arn
    target_endpoint_arn           = aws_dms_endpoint.kinesis_target.endpoint_arn
    table_mappings                = file("${path.module}/table-mappings.json")
    replication_task_settings     = file("${path.module}/task-settings.json")
    # cdc_start_position            = ""

    tags = local.common_tags
  }
