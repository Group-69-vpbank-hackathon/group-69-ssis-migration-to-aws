# VPC Endpoint cho DMS kết nối đến Kinesis
resource "aws_vpc_endpoint" "kinesis" {
  vpc_id            = aws_vpc.glue_vpc.id # VPC chứa DMS
  service_name      = "com.amazonaws.${var.region}.kinesis-streams"
  vpc_endpoint_type = "Interface"
  security_group_ids = [aws_security_group.dms_sg.id]
  subnet_ids        = aws_subnet.private_subnet[*].id # Subnet private
  
  tags = {
    Name = "${var.project_name}-kinesis-endpoint"
  }
}

# DMS Replication Instance
resource "aws_dms_replication_instance" "postgres_cdc" {
  count = length(var.availability_zones)


  allocated_storage          = 50
  apply_immediately          = true
  availability_zone          = var.availability_zones[count.index]
  engine_version             = "3.4.6"
  multi_az                   = false
  publicly_accessible        = false
  replication_instance_class = "dms.t3.medium"
  replication_instance_id    = "${var.project_name}-dms-instance"
  vpc_security_group_ids     = [aws_security_group.dms_sg.id]
  
  tags = {
    Name = "${var.project_name}-dms-instance"
  }
}

# DMS Source Endpoint (Postgres)
resource "aws_dms_endpoint" "postgres_source" {
  endpoint_id   = "${var.project_name}-postgres-source"
  endpoint_type = "source"
  engine_name   = "postgres"
  ssl_mode      = "require"

  username = jsondecode(data.aws_secretsmanager_secret_version.postgres_creds.secret_string)["username"]
  password = jsondecode(data.aws_secretsmanager_secret_version.postgres_creds.secret_string)["password"]

  postgres_settings {
    capture_ddls     = true
    slot_name        = "dms_slot"
    heartbeat_enable = true
    heartbeat_schema = "public"
    max_file_size    = 512
  }
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
resource "aws_dms_replication_task" "postgres_to_kinesis" {
  count = length(var.availability_zones)

  migration_type           = "cdc"
  replication_instance_arn = aws_dms_replication_instance.postgres_cdc[count.index].replication_instance_arn
  replication_task_id      = "${var.project_name}-postgres-to-kinesis-${count.index}"
  source_endpoint_arn      = aws_dms_endpoint.postgres_source.endpoint_arn
  target_endpoint_arn      = aws_dms_endpoint.kinesis_target.endpoint_arn
  table_mappings           = file("${path.module}/files/table-mappings.json")

  tags = {
    Name = "${var.project_name}-postgres-to-kinesis-task-${count.index}"
  }
}