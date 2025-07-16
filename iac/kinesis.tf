resource "aws_kinesis_stream" "data_stream" {
  name             = "${var.project_name}-data-stream"
  shard_count      = 1
  retention_period = 24 # Giờ
  encryption_type  = "KMS"
  
  tags = {
    Name = "${var.project_name}-data-stream"
  }
}