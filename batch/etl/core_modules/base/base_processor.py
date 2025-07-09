import logging
from datetime import timedelta, datetime
from abc import ABC, abstractmethod
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql.functions import lit, col


class BaseProcessor(ABC):
    def __init__(self, args, job_name, data_writer):
        self.args = args
        self.job_name = job_name
        self.data_writer = data_writer
        self.input_path = args.get('input_path')
        self.output_path = args.get('output_path')
        
        self.start_date = args.get('start_date')
        self.end_date = args.get('end_date')
        self.date_range = self._generate_date_ranges(self.start_date, self.end_date)
        
        self.glue_context = GlueContext(SparkContext.getOrCreate())
        self.spark = self.glue_context.spark_session
        self.job = Job(self.glue_context)
        self.job.init(self.job_name, args)
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(self.job_name)

    def _read(self, input_path, partition_key=None, file_format="parquet"):
        self.logger.info(f"Reading {input_path} as {file_format}")

        reader = self.spark.read

        if file_format.lower() == "csv":
            reader = reader.option("header", "true").option("inferSchema", "true")

        df = reader.format(file_format).load(input_path)

        if partition_key and hasattr(self, 'date_range') and self.date_range:
            start = self.date_range[0].strftime("%Y-%m-%d")
            end = self.date_range[-1].strftime("%Y-%m-%d")
            self.logger.info(f"Filtering {partition_key} between {start} and {end}")
            df = df.filter(
                (col(partition_key) >= lit(start)) &
                (col(partition_key) <= lit(end))
            )

        return df
          
    def _write(self, df):
        self.data_writer.write(df)

    @abstractmethod
    def process(self):
        pass

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
    
    def send_notification(self, message):
        # if self.sns_topic_arn:
        #     boto3.client('sns').publish(TopicArn=self.sns_topic_arn, Message=message)
        self.logger.info(f"Notification: {message}")

    def run(self):
        try:
            self.logger.info(f"Starting job: {self.job_name}")
            self.process()
            self.logger.info(f"Job succeeded: {self.job_name}")
        except Exception as e:
            self.send_notification(f"Job failed: {self.job_name} - {str(e)}")
            self.logger.error(f"Job failed: {self.job_name} - {str(e)}", exc_info=True)
            raise
        finally:
            self.job.commit()
