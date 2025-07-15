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
          "StartAt": "collect.TMP_EFZ_FT_AFTER_COB",
          "States": {
            "collect.TMP_EFZ_FT_AFTER_COB": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "postgres_collector_job",
                "Arguments": {
                  "--jdbc_url": "jdbc:postgresql://database-eod-small.cmb4wowm80x3.us-east-1.rds.amazonaws.com:5432/postgres",
                  "--table_name": "public.\"TMP_EFZ_FT_AFTER_COB\"",
                  "--lookback": "0",
                  "--rolling_window": "1",
                  "--date_column": "\"BUSINESS_DATE\"",
                  "--granularity": "daily",
                  "--secret_name": "vph-group69-postgres-2",
                  "--output_path": "s3://vph-group69-landing-zone/TMP_EFZ_FT_AFTER_COB/"
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "States.ALL"
                  ],
                  "IntervalSeconds": 10,
                  "BackoffRate": 2,
                  "MaxAttempts": 0
                }
              ],
              "End": true
            }
          }
        },
        {
          "StartAt": "collect.TMP_EFZ_FT_AFTER_COB_DETAILS",
          "States": {
            "collect.TMP_EFZ_FT_AFTER_COB_DETAILS": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "postgres_collector_job",
                "Arguments": {
                  "--jdbc_url": "jdbc:postgresql://database-eod-small.cmb4wowm80x3.us-east-1.rds.amazonaws.com:5432/postgres",
                  "--table_name": "public.\"TMP_EFZ_FT_AFTER_COB_DETAILS\"",
                  "--lookback": "0",
                  "--rolling_window": "1",
                  "--date_column": "\"BUSINESS_DATE\"",
                  "--secret_name": "vph-group69-postgres-2",
                  "--output_path": "s3://vph-group69-landing-zone/TMP_EFZ_FT_AFTER_COB_DETAILS/"
                }
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "States.ALL"
                  ],
                  "IntervalSeconds": 10,
                  "BackoffRate": 2,
                  "MaxAttempts": 0
                }
              ],
              "End": true
            }
          }
        }
      ],
      "Next": "ParallelLoaderJobs"
    },
    "ParallelLoaderJobs": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "load.TMP_EFZ_FT_AFTER_COB",
          "States": {
            "load.TMP_EFZ_FT_AFTER_COB": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "etl_loader_job",
                "Arguments": {
                  "--lookback": "0",
                  "--rolling_window": "1",
                  "--granularity": "daily",
                  "--partition_key": "date",
                  "--secret_name": "vph-group69-postgres-2",
                  "--output_path": "s3://vph-group69-staging-zone/EOD-batching/TMP_EFZ_FT_AFTER_COB/",
                  "--input_path": "s3://vph-group69-landing-zone/TMP_EFZ_FT_AFTER_COB/",
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
                  "MaxAttempts": 0
                }
              ],
              "End": true
            }
          }
        },
        {
          "StartAt": "load.TMP_EFZ_FT_AFTER_COB_DETAILS_LOADER",
          "States": {
            "load.TMP_EFZ_FT_AFTER_COB_DETAILS_LOADER": {
              "Type": "Task",
              "Resource": "arn:aws:states:::glue:startJobRun.sync",
              "Parameters": {
                "JobName": "etl_loader_job",
                "Arguments": {
                  "--lookback": "0",
                  "--rolling_window": "1",
                  "--granularity": "daily",
                  "--partition_key": "date",
                  "--secret_name": "vph-group69-postgres-2",
                  "--output_path": "s3://vph-group69-staging-zone/EOD-batching/TMP_EFZ_FT_AFTER_COB_DETAILS/",
                  "--input_path": "s3://vph-group69-landing-zone/TMP_EFZ_FT_AFTER_COB_DETAILS/",
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
                  "MaxAttempts": 0
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
          "--temp_views": "after_cob,after_cob_detail",
          "--data_sources": "s3://vph-group69-staging-zone/EOD-batching/TMP_EFZ_FT_AFTER_COB/all,s3://vph-group69-staging-zone/EOD-batching/TMP_EFZ_FT_AFTER_COB_DETAILS/all",
          "--script_file": "s3://vph-group69-glue-jobs/glue_jobs/scripts/cob_script.sql",
          "--output_path": "s3://vph-group69-silver-zone/cob_flatten/",
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
          "MaxAttempts": 0
        }
      ],
      "Next": "LoaderJob"
    },
    "LoaderJob": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "etl_loader_job",
        "Arguments": {
          "--input_path": "s3://vph-group69-silver-zone/cob_flatten/all",
          "--data_writer": "postgres",
          "--jdbc_url": "jdbc:postgresql://database-eod-small.cmb4wowm80x3.us-east-1.rds.amazonaws.com:5432/postgres",
          "--table_name": "public.\"TARGET_TABLE_DEMO\"",
          "--secret_name": "vph-group69-postgres-2",
          "--mode": "append",
          "--batch_size": "2",
          "--target_partitions": "1",
          "--partition_column": "ID"
        }
      },
      "Retry": [
        {
          "ErrorEquals": [
            "States.ALL"
          ],
          "IntervalSeconds": 10,
          "BackoffRate": 2,
          "MaxAttempts": 0
        }
      ],
      "End": true
    }
  }
})

  depends_on = [aws_iam_role_policy_attachment.sfn_glue_policy_attach]
}