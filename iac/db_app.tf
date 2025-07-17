resource "aws_db_parameter_group" "db_app_postgres" {
  name   = "${var.project_name}-db-app-postgres14"
  family = "postgres14"

  parameter {
    name  = "rds.logical_replication"
    value = "1"
    apply_method = "pending-reboot"  # Thêm dòng này
  }
}

# RDS Postgres Instance
resource "aws_db_instance" "db_app" {
  identifier             = "${var.project_name}-db-app"
  engine                 = "postgres"
  engine_version         = "14.15"
  instance_class         = "db.t4g.micro"
  allocated_storage      = 20
  storage_type           = "gp2"
  username               = var.postgres_username
  password               = var.postgres_password
  db_name                = var.postgres_db_name
  db_subnet_group_name   = aws_db_subnet_group.db_app.name
  vpc_security_group_ids = [aws_security_group.db_app_sg.id]
  skip_final_snapshot    = true
  multi_az               = false
  publicly_accessible    = false # Không public access
  backup_retention_period = 7
  parameter_group_name = aws_db_parameter_group.db_app_postgres.name

}

resource "aws_db_subnet_group" "db_app" {
  name       = "${var.project_name}-db_app-subnet-group"
  subnet_ids = [aws_subnet.public_subnet.id, aws_subnet.private_subnet_b.id]
}


# Security Group cho RDS db_app
resource "aws_security_group" "db_app_sg" {
  name        = "${var.project_name}-db_app-sg"
  description = "Security group for db_app RDS"
  vpc_id      = aws_vpc.main_vpc.id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [
      aws_security_group.lambda_sg.id, 
      aws_security_group.bastion_db_app_sg.id
    ]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-db_app-sg"
  }
}

