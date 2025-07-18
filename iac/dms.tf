resource "aws_dms_replication_subnet_group" "glue_subnet_group" {
  replication_subnet_group_id = "${var.project_name}-dms-subnet-group"
  replication_subnet_group_description = "Subnet group for DMS replication instance"
  
  subnet_ids = [
    aws_subnet.private_subnet_a.id,
    aws_subnet.private_subnet_b.id
  ]

  tags = {
    Name = "${var.project_name}-dms-subnet-group"
  }
}


# DMS Replication Instance
resource "aws_dms_replication_instance" "eod_cdc" {
  allocated_storage            = 50
  apply_immediately            = true
  engine_version               = "3.5.4"
  multi_az                     = true # BẬT Multi-AZ
  publicly_accessible          = false
  replication_instance_class   = "dms.t3.medium"
  replication_instance_id      = "${var.project_name}-dms-eod-cdc-instance"
  replication_subnet_group_id  = aws_dms_replication_subnet_group.glue_subnet_group.replication_subnet_group_id
  vpc_security_group_ids       = [aws_security_group.dms_sg.id]

  lifecycle {
    prevent_destroy       = false
    create_before_destroy = true
    ignore_changes        = [replication_instance_class]
  }

  tags = {
    Name = "${var.project_name}-dms-instance"
  }

}


# DMS Source Endpoint (eod)
resource "aws_dms_endpoint" "eod_source" {
  endpoint_id   = "${var.project_name}-eod-source"
  endpoint_type = "source"
  engine_name   = "postgres"
  ssl_mode      = "require"

  server_name   = aws_db_instance.eod.address
  port          = 5432
  database_name = var.postgres_db_name

  username = jsondecode(aws_secretsmanager_secret_version.eod_creds_version.secret_string)["db_username"]
  password = jsondecode(aws_secretsmanager_secret_version.eod_creds_version.secret_string)["db_password"]

}



# DMS Target Endpoint (Kinesis)
resource "aws_dms_endpoint" "kinesis_target" {
  endpoint_id   = "${var.project_name}-kinesis-target"
  endpoint_type = "target"
  engine_name   = "kinesis"
  
  kinesis_settings {
    message_format          = "json"
    service_access_role_arn = aws_iam_role.dms_kinesis_role.arn
    stream_arn             = aws_kinesis_stream.data_stream.arn
  }
}

# DMS Replication Task
resource "aws_dms_replication_task" "eod_to_kinesis" {
  migration_type           = "full-load-and-cdc"
  replication_instance_arn = aws_dms_replication_instance.eod_cdc.replication_instance_arn
  replication_task_id      = "${var.project_name}-eod-to-kinesis"
  source_endpoint_arn      = aws_dms_endpoint.eod_source.endpoint_arn
  target_endpoint_arn      = aws_dms_endpoint.kinesis_target.endpoint_arn
  table_mappings           = file("${path.module}/files/table-mappings.json")

  tags = {
    Name = "${var.project_name}-eod-to-kinesis-task"
  }
}


# Security Group cho DMS
resource "aws_security_group" "dms_sg" {
  name        = "${var.project_name}-dms-sg"
  description = "Security group for DMS"
  vpc_id      = aws_vpc.main_vpc.id
  
  # Cho phép DMS kết nối đến eod
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-dms-sg"
  }
}