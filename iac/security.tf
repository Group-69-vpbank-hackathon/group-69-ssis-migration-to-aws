resource "aws_security_group" "glue_sg" {
  name        = "${var.project_name}-glue-sg"
  description = "Security group for Glue jobs running in VPC"
  vpc_id      = aws_vpc.glue_vpc.id
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    self      = true
  }
  
  # Tối ưu egress rule cho bảo mật tốt hơn
  egress {
    from_port   = 5432  # Chỉ mở port PostgreSQL
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.postgres_vpc.cidr_block]  # Chỉ cho phép đến RDS VPC
  }
  
  # Thêm rule egress cho các dịch vụ AWS cần thiết
  egress {
    from_port   = 443  # HTTPS
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Cho phép ra các dịch vụ AWS
  }
  tags = {
    Name = "${var.project_name}-glue-sg"
  }
}


# Security Group cho RDS Postgres
resource "aws_security_group" "postgres_sg" {
  name        = "${var.project_name}-postgres-sg"
  description = "Security group for Postgres RDS"
  vpc_id      = aws_vpc.postgres_vpc.id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [aws_security_group.dms_sg.id, aws_security_group.glue_sg.id] 
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-postgres-sg"
  }
}

# Security Group cho DMS
resource "aws_security_group" "dms_sg" {
  name        = "${var.project_name}-dms-sg"
  description = "Security group for DMS"
  vpc_id      = aws_vpc.glue_vpc.id
  
  # Cho phép DMS kết nối đến Postgres
  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.postgres_vpc.cidr_block]
  }
  
  # Cho phép DMS gửi data đến Kinesis qua VPC Endpoint
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    security_groups = [aws_security_group.kinesis_endpoint_sg.id]
  }
  
  tags = {
    Name = "${var.project_name}-dms-sg"
  }
}

resource "aws_security_group" "kinesis_endpoint_sg" {
  name        = "kinesis-endpoint-sg"
  description = "Security group for Kinesis endpoint"
  vpc_id      = aws_vpc.glue_vpc.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    security_groups = [aws_security_group.dms_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

