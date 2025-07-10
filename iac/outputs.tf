output "glue_job_name" {
  description = "Glue Job created by Terraform"
  value       = aws_glue_job.csv_collector.name
}
