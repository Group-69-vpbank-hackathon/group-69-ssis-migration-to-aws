# RDS Postgres Instance
resource "aws_db_instance" "db_app" {
  identifier             = "${var.project_name}-db-app"
  engine                 = "postgres"
  engine_version         = "15.12"
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
}

resource "aws_db_subnet_group" "db_app" {
  name       = "${var.project_name}-db-app-subnet-group"
  subnet_ids = aws_subnet.db_app_subnet[*].id
}

# =========================== VPC cho db_app (isolated) ==================================
resource "aws_vpc" "db_app_vpc" {
  cidr_block           = "10.2.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${var.project_name}-db_app-vpc"
  }
}

# Subnet private cho RDS
resource "aws_subnet" "db_app_subnet" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.db_app_vpc.id
  cidr_block        = "10.2.${count.index + 1}.0/24"
  availability_zone = var.availability_zones[count.index]
  tags = {
    Name = "${var.project_name}-db_app-subnet-${count.index + 1}"
  }
}

# Route table riêng cho subnet db_app
resource "aws_route_table" "db_app_private_rt" {
  vpc_id = aws_vpc.db_app_vpc.id

  tags = {
    Name = "${var.project_name}-db_app-private-rt"
  }
}

# Gán route table này cho tất cả subnet db_app
resource "aws_route_table_association" "db_app_private_assoc" {
  count          = length(aws_subnet.db_app_subnet)
  subnet_id      = aws_subnet.db_app_subnet[count.index].id
  route_table_id = aws_route_table.db_app_private_rt.id
}

# Security Group cho RDS db_app
resource "aws_security_group" "db_app_sg" {
  name        = "${var.project_name}-db-app-sg"
  description = "Security group for db_app RDS"
  vpc_id      = aws_vpc.db_app_vpc.id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [aws_security_group.lambda_sg.id, aws_security_group.glue_sg.id] 
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


# ====================  VPC Peering giữa main_vpc và db_app_vpc ==============================
resource "aws_vpc_peering_connection" "main_vpc_db_app_peering_conn" {
  peer_vpc_id = aws_vpc.db_app_vpc.id
  vpc_id      = aws_vpc.main_vpc.id
  auto_accept = true
  tags = {
    Name = "${var.project_name}-glue-db_app-peering"
  }
}

# Update route table của main_vpc
resource "aws_route" "glue_to_db_app" {
  route_table_id            = aws_route_table.private_rt.id
  destination_cidr_block    = aws_vpc.db_app_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.main_vpc_db_app_peering_conn.id
}

# Update route table của db_app_vpc
resource "aws_route" "rdb_app_to_glue" {
  route_table_id            = aws_route_table.db_app_private_rt.id
  destination_cidr_block    = aws_vpc.main_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.main_vpc_db_app_peering_conn.id
}


# public subnet
resource "aws_subnet" "db_app_public_subnet" {
  vpc_id                  = aws_vpc.db_app_vpc.id
  cidr_block              = "10.2.100.0/24"
  availability_zone       = var.availability_zones[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-db-app-public-subnet"
  }
}

resource "aws_internet_gateway" "db_app_igw" {
  vpc_id = aws_vpc.db_app_vpc.id

  tags = {
    Name = "${var.project_name}-db-app-igw"
  }
}


resource "aws_route_table" "db_app_public_rt" {
  vpc_id = aws_vpc.db_app_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.db_app_igw.id
  }

  tags = {
    Name = "${var.project_name}-db-app-public-rt"
  }
}

resource "aws_route_table_association" "db_app_public_assoc" {
  subnet_id      = aws_subnet.db_app_public_subnet.id
  route_table_id = aws_route_table.db_app_public_rt.id
}
