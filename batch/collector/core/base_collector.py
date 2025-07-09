import sys
from datetime import timedelta, datetime
import json
import boto3
import logging
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from awsglue.utils import getResolvedOptions

class BaseCollector:
    """BaseCollector is an abstract class for reading data from various sources and writing to S3."""

    def __init__(self, args, job_name):
        self.args = args
        self.job_name = job_name
        self.output_path = args['output_path']
        self.sns_topic_arn = args.get('sns_topic_arn')
        
        self.start_date = args.get('start_date')
        self.end_date = args.get('end_date')
        self.date_column = args.get('date_column')
        self.date_column_type = args.get('date_column_type', 'date')
        self.date_range = self._generate_date_ranges(self.start_date, self.end_date)

        self.glue_context = GlueContext(SparkContext.getOrCreate())
        self.spark = self.glue_context.spark_session
        self.job = Job(self.glue_context)
        self.job.init(self.job_name, args)

        self.logger = self._setup_logger()

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(self.job_name)

    def get_secret(self, secret_name):
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])

    def write_to_s3(self, df, format="parquet", mode="overwrite", output_file = None):
        self.logger.info(f"Writing to S3: {output_file}")
        df.write.mode(mode).format(format).save(output_file)

    def send_notification(self, message):
        # if self.sns_topic_arn:
        #     boto3.client('sns').publish(TopicArn=self.sns_topic_arn, Message=message)
        self.logger.info(f"Notification: {message}")

    def _generate_date_ranges(self, start_date, end_date, date_format="%Y-%m-%d"):
        """Generate list of dates between start_date and end_date (inclusive)."""
        if not start_date or not end_date:
            return []
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, date_format)
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, date_format)

        report_dates = []
        next_date = start_date
        delta = timedelta(days=1)

        while next_date <= end_date:
            report_dates.append(next_date)
            next_date += delta
        return report_dates
    
    def run_with_exception_handling(self):
        try:
            self.run()
            self.send_notification(f"Glue Job succeeded: {self.job_name}")
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
