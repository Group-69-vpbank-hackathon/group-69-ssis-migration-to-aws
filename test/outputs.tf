output "glue_job_name" {
  description = "Glue Job created by Terraform"
  value       = aws_glue_job.csv_collector.name
}
# VPC Outputs for DMS to use
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.glue_vpc.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.glue_vpc.cidr_block
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = [aws_subnet.public_subnet_1.id, aws_subnet.public_subnet_2.id]
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.igw.id
}

output "nat_gateway_ids" {
  description = "IDs of the NAT Gateways"
  value       = [aws_nat_gateway.nat_gw_1.id, aws_nat_gateway.nat_gw_2.id]
}
