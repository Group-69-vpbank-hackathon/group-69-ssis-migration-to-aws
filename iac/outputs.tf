output "glue_jobs" {
  description = "Glue Jobs created by Terraform"
  value = "all"
}

output "eod_db" {
  description = "EOD postgres created by Terraform"
  value = "all"
}

output "app_db" {
  description = "APP_DB postgres created by Terraform"
  value = "all"
}

output "lambda" {
  description = "lambda functions created by Terraform"
  value = "all"
}

output "sqs" {
  description = "sqs dlq created by Terraform"
  value = "all"
}


