variable "project_name" {
  description = "Tên dự án, dùng để đặt tên các tài nguyên mạng"
  type        = string
  default     = "vph-group69"
}

variable "region" {
  description = "region"
  type        = string
  default     = "us-east-1"
}

variable "availability_zones" {
  description = "List of Availability Zones to use"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "postgres_username" {
  description = "Master username for RDS Postgres"
  type        = string
  default     = "postgres"
}

variable "postgres_password" {
  description = "Master password for RDS Postgres"
  type        = string
  sensitive   = true
  default     = "postgres"
}

variable "postgres_db_name" {
  description = "Database name for RDS Postgres"
  type        = string
  sensitive   = true
  default     = "postgres"
}

variable "glue_bucket" {
  description = "S3 bucket để chứa glue scripts"
  type        = string
  default     = "vph-group69-glue-jobs-bucket"
}

variable "data_source_bucket" {
  description = "S3 bucket để chứa data nguồn mô phỏng"
  type        = string
  default     = "vph-group69-sample-data-source"
}

variable "landing_zone_bucket" {
  description = "S3 bucket để chứa tất cả data đc nạp"
  type        = string
  default     = "vph-group69-landing-zone"
}

variable "staging_zone_bucket" {
  description = "S3 bucket để chứa staging data"
  type        = string
  default     = "vph-group69-staging-zone"
}

variable "silver_zone_bucket" {
  description = "S3 bucket để chứa data đã làm sạch"
  type        = string
  default     = "vph-group69-silver-zone"
}

variable "gold_zone_bucket" {
  description = "S3 bucket để chứa data đã xử lí xong"
  type        = string
  default     = "vph-group69-gold-zone"
}

variable "backup_streaming_zone_bucket" {
  description = "S3 bucket để chứa data backup cho stream"
  type        = string
  default     = "vph-group69-backup-streaming-zone"
}

variable "lambda_artifacts_bucket" {
  description = "S3 bucket để chứa code lambda"
  type        = string
  default     = "vph-group69-lambda-artifacts"
}

variable "streaming_failover_bucket" {
  description = "S3 bucket để chứa data stream failover"
  type        = string
  default     = "vph-group69-streaming-failover"
}

variable "terraform_backend_bucket" {
  description = "S3 bucket để terraform_backend"
  type        = string
  default     = "vph-group69-terraform-backend"
}

variable "bastion_ami_id" {
  description = "AMI ID for bastion EC2 (e.g. Amazon Linux 2023)"
  type        = string
  default     = "ami-0c101f26f147fa7fd"
}

variable "ssh_key_bastion_eod" {
  description = "AMI ID for bastion EC2 (e.g. Amazon Linux 2023)"
  type        = string
  default     = "bastion-eod-key"
}

variable "ssh_key_bastion_db_app" {
  description = "AMI ID for bastion EC2 (e.g. Amazon Linux 2023)"
  type        = string
  default     = "bastion-db-app-key"
}

variable "ssh_key_bastion_main" {
  description = "AMI ID for bastion EC2 (e.g. Amazon Linux 2023)"
  type        = string
  default     = "bastion-main-key"
}

