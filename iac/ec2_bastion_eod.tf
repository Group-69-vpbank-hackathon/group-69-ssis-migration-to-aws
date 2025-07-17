resource "aws_instance" "bastion_eod" {
  ami                         = var.bastion_ami_id     # Ví dụ Amazon Linux 2023 AMI
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.eod_public_subnet.id
  vpc_security_group_ids      = [aws_security_group.bastion_eod_sg.id]
  associate_public_ip_address = true
  key_name                    = var.ssh_key_bastion_eod

  tags = {
    Name = "${var.project_name}-bastion-eod"
  }
}


resource "aws_security_group" "bastion_eod_sg" {
  name        = "${var.project_name}-bastion-sg"
  description = "Allow SSH access and outbound to RDS"
  vpc_id      = aws_vpc.eod_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-bastion-sg"
  }
}
