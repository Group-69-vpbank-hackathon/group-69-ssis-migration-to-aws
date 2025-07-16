resource "aws_vpc" "glue_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true # Cần thiết cho một số dịch vụ
  enable_dns_support   = true # Cần thiết cho một số dịch vụ
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.glue_vpc.id
  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.glue_vpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true # Không thực sự cần cho NAT GW nhưng là thông lệ tốt
  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.glue_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = "${var.project_name}-private-subnet"
  }
}

resource "aws_eip" "nat_eip" {
  depends_on = [aws_internet_gateway.igw]
}

resource "aws_nat_gateway" "nat_gw" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet.id
  tags = {
    Name = "${var.project_name}-nat-gw"
  }
  depends_on = [aws_internet_gateway.igw]
}


resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.glue_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.glue_vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gw.id
  }
  tags = {
    Name = "${var.project_name}-private-rt"
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private_rt.id
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.glue_vpc.id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private_rt.id]
  tags = {
    Name = "${var.project_name}-s3-endpoint"
  }
}



# =========================== VPC cho Postgres (isolated) ==================================
resource "aws_vpc" "postgres_vpc" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${var.project_name}-postgres-vpc"
  }
}

# Subnet private cho RDS
resource "aws_subnet" "postgres_subnet" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.postgres_vpc.id
  cidr_block        = "10.1.${count.index + 1}.0/24"
  availability_zone = var.availability_zones[count.index]
  tags = {
    Name = "${var.project_name}-postgres-subnet-${count.index + 1}"
  }
}

# Route table riêng cho subnet Postgres
resource "aws_route_table" "postgres_private_rt" {
  vpc_id = aws_vpc.postgres_vpc.id

  tags = {
    Name = "${var.project_name}-postgres-private-rt"
  }
}

# Gán route table này cho tất cả subnet Postgres
resource "aws_route_table_association" "postgres_private_assoc" {
  count          = length(aws_subnet.postgres_subnet)
  subnet_id      = aws_subnet.postgres_subnet[count.index].id
  route_table_id = aws_route_table.postgres_private_rt.id
}



# ====================  VPC Peering giữa glue_vpc và postgres_vpc ==============================
resource "aws_vpc_peering_connection" "glue_rds_peering_conn" {
  peer_vpc_id = aws_vpc.postgres_vpc.id
  vpc_id      = aws_vpc.glue_vpc.id
  auto_accept = true
  tags = {
    Name = "${var.project_name}-glue-postgres-peering"
  }
}

# Update route table của glue_vpc
resource "aws_route" "glue_to_rds" {
  route_table_id            = aws_route_table.private_rt.id
  destination_cidr_block    = aws_vpc.postgres_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.glue_rds_peering_conn.id
}

# Update route table của postgres_vpc
resource "aws_route" "rds_to_glue" {
  route_table_id            = aws_vpc.postgres_vpc.postgres_private_rt.id
  destination_cidr_block    = aws_vpc.glue_vpc.cidr_block
  vpc_peering_connection_id = aws_vpc_peering_connection.glue_rds_peering_conn.id
}