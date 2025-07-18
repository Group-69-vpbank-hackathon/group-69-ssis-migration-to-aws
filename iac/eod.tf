resource "aws_db_parameter_group" "eod_postgres" {
  name   = "${var.project_name}-eod-postgres14"
  family = "postgres14"

  parameter {
    name  = "rds.logical_replication"
    value = "1"
    apply_method = "pending-reboot"  # Thêm dòng này
  }
}

# RDS Postgres Instance
resource "aws_db_instance" "eod" {
  identifier             = "${var.project_name}-eod"
  engine                 = "postgres"
  engine_version         = "14.15"
  instance_class         = "db.t4g.micro"
  allocated_storage      = 20
  storage_type           = "gp2"
  username               = var.postgres_username
  password               = var.postgres_password
  db_name                = var.postgres_db_name
  db_subnet_group_name   = aws_db_subnet_group.eod.name
  vpc_security_group_ids = [aws_security_group.eod_sg.id]
  skip_final_snapshot    = true
  multi_az               = false
  publicly_accessible    = false # Không public access
  backup_retention_period = 7
  parameter_group_name = aws_db_parameter_group.eod_postgres.name

}

resource "aws_db_subnet_group" "eod" {
  name       = "${var.project_name}-eod-subnet-group"
  subnet_ids = [aws_subnet.private_subnet_a.id, aws_subnet.private_subnet_b.id]
}


# Security Group cho RDS eod
resource "aws_security_group" "eod_sg" {
  name        = "${var.project_name}-eod-sg"
  description = "Security group for eod RDS"
  vpc_id      = aws_vpc.main_vpc.id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [
      aws_security_group.dms_sg.id, 
      aws_security_group.glue_sg.id, 
      aws_security_group.bastion_public_sg.id
    ]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-eod-sg"
  }
}

