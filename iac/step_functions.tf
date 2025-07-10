resource "aws_sfn_state_machine" "etl_orchestrator" {
  name     = "${var.project_name}-etl-orchestrator"
  role_arn = aws_iam_role.sfn_exec_role.arn

  definition = jsonencode({
  "Comment": "Run CSV Collector Jobs in parallel, then run Transformer Job",
  "StartAt": "ParallelCollectorJobs",
  "States": {
    "ParallelCollectorJobs": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "UserCsvCollectorJob",
          "States": {
            "UserCsvCollectorJob": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "csv_collector_job",
                "Arguments": {
                  "--input_path": "s3://vph-group69-sample-data-source/users/users.csv",
                  "--output_path": "s3://vph-group69-landing-zone/users/"
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "States.ALL"
                  ],
                  "IntervalSeconds": 10,
                  "BackoffRate": 2,
                  "MaxAttempts": 3
                }
              ],
              "End": true
            }
          }
        },
        {
          "StartAt": "TransactionCsvCollectorJob",
          "States": {
            "TransactionCsvCollectorJob": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "csv_collector_job",
                "Arguments": {
                  "--input_path": "s3://vph-group69-sample-data-source/transactions/transactions.csv",
                  "--output_path": "s3://vph-group69-landing-zone/transactions/"
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "States.ALL"
                  ],
                  "IntervalSeconds": 10,
                  "BackoffRate": 2,
                  "MaxAttempts": 3
                }
              ],
              "End": true
            }
          }
        }
      ],
      "Next": "TransformerJob"
    },
    "TransformerJob": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "etl_transformer_job",
        "Arguments": {
          "--temp_views": "users,transactions",
          "--data_sources": "s3://vph-group69-landing-zone/users/all,s3://vph-group69-landing-zone/transactions/all",
          "--script_file": "s3://vph-group69-glue-jobs/glue_jobs/scripts/users_trans.sql",
          "--output_path": "s3://vph-group69-silver-zone/transactions_enriched/",
          "--data_writer": "s3"
        }
      },
      "Retry": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "IntervalSeconds": 10,
          "BackoffRate": 2,
          "MaxAttempts": 3
        }
      ],
      "End": true
    }
  }
})

  depends_on = [aws_iam_role_policy_attachment.sfn_glue_policy_attach]
}