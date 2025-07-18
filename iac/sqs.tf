resource "aws_sqs_queue" "dlq_queue_records" {
  name = "dlq_queue_records"
  visibility_timeout_seconds = 600

}

resource "aws_sqs_queue" "dlq_queue_metadata" {
  name = "dlq_queue_metadata"
  visibility_timeout_seconds = 600
}
