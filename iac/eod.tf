# RDS Postgres Instance
resource "aws_db_instance" "eod" {
  identifier             = "${var.project_name}-eod"
  engine                 = "postgres"
  engine_version         = "15.12"
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
}

resource "aws_db_subnet_group" "eod" {
  name       = "${var.project_name}-eod-subnet-group"
  subnet_ids = aws_subnet.eod_subnet[*].id
}

# =========================== VPC cho eod (isolated) ==================================
resource "aws_vpc" "eod_vpc" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${var.project_name}-eod-vpc"
  }
}

# Subnet private cho RDS
resource "aws_subnet" "eod_subnet" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.eod_vpc.id
  cidr_block        = "10.1.${count.index + 1}.0/24"
  availability_zone = var.availability_zones[count.index]
  tags = {
    Name = "${var.project_name}-eod-subnet-${count.index + 1}"
  }
}

# Route table riêng cho subnet eod
resource "aws_route_table" "eod_private_rt" {
  vpc_id = aws_vpc.eod_vpc.id

  tags = {
    Name = "${var.project_name}-eod-private-rt"
  }
}

# Gán route table này cho tất cả subnet eod
resource "aws_route_table_association" "eod_private_assoc" {
  count          = length(aws_subnet.eod_subnet)
  subnet_id      = aws_subnet.eod_subnet[count.index].id
  route_table_id = aws_route_table.eod_private_rt.id
}

# public subnet
resource "aws_subnet" "eod_public_subnet" {
  vpc_id                  = aws_vpc.eod_vpc.id
  cidr_block              = "10.1.100.0/24"
  availability_zone       = var.availability_zones[0]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-eod-public-subnet"
  }
}

resource "aws_internet_gateway" "eod_igw" {
  vpc_id = aws_vpc.eod_vpc.id

  tags = {
    Name = "${var.project_name}-eod-igw"
  }
}


resource "aws_route_table" "eod_public_rt" {
  vpc_id = aws_vpc.eod_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.eod_igw.id
  }

  tags = {
    Name = "${var.project_name}-eod-public-rt"
  }
}

resource "aws_route_table_association" "eod_public_assoc" {
  subnet_id      = aws_subnet.eod_public_subnet.id
  route_table_id = aws_route_table.eod_public_rt.id
}




# Security Group cho RDS eod
resource "aws_security_group" "eod_sg" {
  name        = "${var.project_name}-eod-sg"
  description = "Security group for eod RDS"
  vpc_id      = aws_vpc.eod_vpc.id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [
      aws_security_group.dms_sg.id, 
      aws_security_group.glue_sg.id, 
      aws_security_group.bastion_eod_sg.id
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

# ====================  VPC Peering giữa main_vpc và eod_vpc ==============================
resource "aws_vpc_peering_connection" "main_vpc_eod_peering_conn" {
  peer_vpc_id = aws_vpc.eod_vpc.id
  vpc_id      = aws_vpc.main_vpc.id
  auto_accept = true
  tags = {
    Name = "${var.project_name}-glue-eod-peering"
  }
}

# Update route table của main_vpc
resource "aws_route" "glue_to_eod" {
  route_table_id            = aws_route_table.private_rt.id
  destination_cidr_block    = aws_vpc.eod_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.main_vpc_eod_peering_conn.id
}

# Update route table của eod_vpc
resource "aws_route" "eod_to_glue" {
  route_table_id            = aws_route_table.eod_private_rt.id
  destination_cidr_block    = aws_vpc.main_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.main_vpc_eod_peering_conn.id
}