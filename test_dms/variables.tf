variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "data-pipeline"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  default     = "dev"
}

variable "source_database_endpoint" {
  description = "Source database endpoint for DMS"
  type        = string
}

# variable "target_database_endpoint" {
#   description = "Target database endpoint"
#   type        = string
# }

variable "github_token" {
  description = "GitHub token for CodePipeline"
  type        = string
  sensitive   = true
  default     = ""
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs for Lambda and DMS"
  type        = list(string)
}


variable "db_port" {
  description = "Database port for DMS source endpoint"
  type        = number
  default     = 5432
}

variable "db_name" {
  description = "Database name for DMS source endpoint"
  type        = string
  default     = ""
}

variable "db_username" {
  description = "Database username for DMS source endpoint"
  type        = string
  default     = ""
}

variable "db_password" {
  description = "Database password for DMS source endpoint"
  type        = string
  sensitive   = true
  default     = ""
} 

variable "glue_bucket" {
  type        = string
  description = "S3 bucket chứa script cho Glue"
}