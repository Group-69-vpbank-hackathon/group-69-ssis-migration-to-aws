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

variable "glue_bucket" {
  description = "S3 bucket để chứa glue scripts"
  type        = string
  default     = "vph-group69-glue-jobs"
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
