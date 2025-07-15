output "kinesis_stream_arn" {
  description = "ARN of the Kinesis Data Stream"
  value       = aws_kinesis_stream.data_stream.arn
}

output "data_lake_bucket" {
  description = "Name of the data lake S3 bucket"
  value       = aws_s3_bucket.data_lake.bucket
}

output "backup_zone_bucket" {
  description = "Name of the backup zone S3 bucket"
  value       = aws_s3_bucket.backup_zone.bucket
}



output "dms_instance_id" {
  description = "ID of the DMS replication instance"
  value       = aws_dms_replication_instance.dms_instance.replication_instance_id
}

output "private_subnet_ids" {
  description = "IDs of private subnets for use in other modules"
  value       = aws_subnet.private[*].id
}

output "lambda_sg_id" {
  description = "ID of the Lambda security group"
  value       = aws_security_group.lambda_sg.id
} 