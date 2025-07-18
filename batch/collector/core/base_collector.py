import sys
from datetime import timedelta, datetime
import json
import boto3
import logging
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from common.utils.helper import generate_date_ranges


class BaseCollector:
    """BaseCollector is an abstract class for reading data from various sources and writing to S3."""

    def __init__(self, args, job_name):
        self.args = args
        self.job_name = job_name
        self.logger = self._setup_logger()

        self.output_path = args["output_path"]
        self.sns_topic_arn = args.get("sns_topic_arn")

        self.lookback = args.get("lookback")
        self.rolling_window = args.get("rolling_window")

        self.start_date = args.get("start_date")
        self.end_date = args.get("end_date")

        self.date_column = args.get("date_column")
        self.date_column_type = (args.get("date_column_type") or "date").lower()
        self.date_format = (args.get("date_format") or "default").lower()
        self.date_range = self._calculate_date_range()

        self.glue_context = GlueContext(SparkContext.getOrCreate())
        self.spark = self.glue_context.spark_session
        self.job = Job(self.glue_context)
        self.job.init(self.job_name, args)

    def _calculate_date_range(self):
        if self.start_date and self.end_date:
            self.logger.info(
                f"Using start_date: {self.start_date} and end_date: {self.end_date}"
            )
            return generate_date_ranges(
                self.start_date, self.end_date, self.date_format
            )
        if self.lookback is not None and self.rolling_window is not None:
            self.logger.info(f"Using lookback: {self.lookback} and rolling_window:")
            self.end_date = datetime.now() - timedelta(days=int(self.lookback))
            self.start_date = (
                self.end_date - timedelta(days=int(self.rolling_window))
            ).strftime("%Y-%m-%d")
            self.end_date = self.end_date.strftime("%Y-%m-%d")
            self.logger.info(
                f"Calculated start_date: {self.start_date} and end_date: {self.end_date}"
            )
            return generate_date_ranges(self.start_date, self.end_date, "default")

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(self.job_name)

    def get_secret(self, secret_name):
        client = boto3.client("secretsmanager")
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])

    def write_to_s3(self, df, format="parquet", mode="overwrite", output_file=None):
        self.logger.info(f"Writing to S3: {output_file}")
        df.write.mode(mode).format(format).save(output_file)

    def send_notification(self, message):
        # if self.sns_topic_arn:
        #     boto3.client('sns').publish(TopicArn=self.sns_topic_arn, Message=message)
        self.logger.info(f"Notification: {message}")

    def run_with_exception_handling(self):
        try:
            self.run()
            self.logger.info(f"Glue Job succeeded: {self.job_name}")
        except Exception as e:
            error_message = f"Glue Job failed: {self.job_name} - {str(e)}"
            self.logger.error(error_message, exc_info=True)
            self.send_notification(error_message)
            raise
        finally:
            self.job.commit()

    def _get_output_path(self, event_date):
        event_date_str = event_date.strftime("%Y-%m-%d")
        return f"{self.output_path}/date={event_date_str}"

    def run(self):
        raise NotImplementedError("Subclasses must implement the run() method.")
