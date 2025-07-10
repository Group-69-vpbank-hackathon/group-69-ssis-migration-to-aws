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
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "${var.project_name}-glue-sg"
  }
}