import sys
import logging
from abc import ABC, abstractmethod
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from awsglue.utils import getResolvedOptions

class BaseProcessor(ABC):
    def __init__(self, args, job_name):
        self.args = args
        self.job_name = job_name
        self.input_path = args.get('input_path')
        self.output_path = args.get('output_path')
        self.file_format = args.get('file_format', 'iceberg')
        self.glue_context = GlueContext(SparkContext.getOrCreate())
        self.spark = self.glue_context.spark_session
        self.job = Job(self.glue_context)
        self.job.init(self.job_name, args)
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(self.job_name)

    def read_df(self, path=None, file_format=None):
        path = path or self.input_path
        file_format = file_format or self.file_format
        return self.spark.read.format(file_format).load(path)

    def write_df(self, df, path=None, file_format=None, mode="overwrite"):
        path = path or self.output_path
        file_format = file_format or self.file_format
        df.write.mode(mode).format(file_format).save(path)

    @abstractmethod
    def process(self):
        pass

    def run(self):
        try:
            self.logger.info(f"Starting job: {self.job_name}")
            self.process()
            self.logger.info(f"Job succeeded: {self.job_name}")
        except Exception as e:
            self.logger.error(f"Job failed: {self.job_name} - {str(e)}", exc_info=True)
            raise
        finally:
            self.job.commit()
