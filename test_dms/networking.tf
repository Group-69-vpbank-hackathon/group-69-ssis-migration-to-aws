############################
# Data sources to reference Glue VPC
############################

# Option 1: Using remote state (recommended if using same backend)
# data "terraform_remote_state" "glue" {
#   backend = "s3"  # or whatever backend you're using
#   config = {
#     bucket = "your-terraform-state-bucket"
#     key    = "test/terraform.tfstate"
#     region = "us-east-1"
#   }
# }

# Option 2: Using data sources to lookup existing resources
data "aws_vpc" "glue_vpc" {
  filter {
    name   = "tag:Name"
    values = ["vph-group69_001-vpc"]  # This should match the VPC name from Glue
  }
}

data "aws_subnets" "private_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.glue_vpc.id]
  }
  
  filter {
    name   = "tag:Name"
    values = ["*private*"]
  }
}

data "aws_subnets" "public_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.glue_vpc.id]
  }
  
  filter {
    name   = "tag:Name"
    values = ["*public*"]
  }
}

############################
# SECURITY GROUPS
############################

resource "aws_security_group" "dms_sg" {
  name_prefix = "${local.name_prefix}-dms-"
  vpc_id      = data.aws_vpc.glue_vpc.id
  description = "Security group for DMS replication instance"

  # Inbound rules for database connections
  ingress {
    description = "PostgreSQL from VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.glue_vpc.cidr_block]
  }

  ingress {
    description = "PostgreSQL from external (Supabase)"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Consider restricting to Supabase IP ranges if known
  }

  # Outbound rules
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-dms-sg"
  })
}

resource "aws_security_group" "lambda_sg" {
  name_prefix = "${local.name_prefix}-lambda-"
  vpc_id      = data.aws_vpc.glue_vpc.id
  description = "Security group for Lambda functions"

  # Inbound rules - allow traffic from within VPC
  ingress {
    description = "All traffic from VPC"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [data.aws_vpc.glue_vpc.cidr_block]
  }

  # Outbound rules
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-lambda-sg"
  })
}

############################
# VPC Endpoints (if needed for DMS)
############################

# VPC Endpoint for DMS (if not already exists in Glue VPC)
resource "aws_vpc_endpoint" "dms" {
  vpc_id              = data.aws_vpc.glue_vpc.id
  service_name        = "com.amazonaws.us-east-1.dms"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = data.aws_subnets.private_subnets.ids
  security_group_ids  = [aws_security_group.dms_sg.id]
  
  private_dns_enabled = true
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-dms-endpoint"
  })
}

# VPC Endpoint for Kinesis (if not already exists)
resource "aws_vpc_endpoint" "kinesis_streams" {
  vpc_id              = data.aws_vpc.glue_vpc.id
  service_name        = "com.amazonaws.us-east-1.kinesis-streams"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = data.aws_subnets.private_subnets.ids
  security_group_ids  = [aws_security_group.dms_sg.id]
  
  private_dns_enabled = true
  
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-kinesis-streams-endpoint"
  })
}

############################
# Outputs for reference
############################

output "vpc_id" {
  description = "ID of the shared VPC"
  value       = data.aws_vpc.glue_vpc.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the shared VPC"
  value       = data.aws_vpc.glue_vpc.cidr_block
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = data.aws_subnets.private_subnets.ids
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = data.aws_subnets.public_subnets.ids
}

output "dms_security_group_id" {
  description = "ID of the DMS security group"
  value       = aws_security_group.dms_sg.id
}

output "lambda_security_group_id" {
  description = "ID of the Lambda security group"
  value       = aws_security_group.lambda_sg.id
}
