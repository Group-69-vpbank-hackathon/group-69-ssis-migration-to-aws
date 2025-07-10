terraform {
  backend "s3" {
    bucket         = "vph-group69-terraform-backend"
    key            = "glue_jobs/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}
