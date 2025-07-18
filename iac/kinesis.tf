resource "aws_kinesis_stream" "data_stream" {
  name             = "${var.project_name}-data-stream"
  shard_count      = 1
  retention_period = 24 # Giờ
  encryption_type  = "NONE"
  
  tags = {
    Name = "${var.project_name}-data-stream"
  }
}

resource "aws_security_group" "kinesis_endpoint_sg" {
  name        = "kinesis-endpoint-sg"
  description = "Security group for Kinesis endpoint"
  vpc_id      = aws_vpc.main_vpc.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    security_groups = [aws_security_group.dms_sg.id, aws_security_group.lambda_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}