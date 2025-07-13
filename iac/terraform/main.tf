provider "aws" {
  region = "us-east-1"
}

module "streaming_backup" {
  source = "./modules/streaming_backup"
  bucket_name        = "backup-streaming-zone"
  stream_name        = "vph-kds-stream"
  firehose_name      = "streaming-to-s3-firehose"
}
