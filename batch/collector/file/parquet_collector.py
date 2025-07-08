import sys
from awsglue.utils import getResolvedOptions
from datetime import datetime

from collector.core.file_collector import FileCollector

class ParquetCollector(FileCollector):
    JOB_NAME = "parquet_collector_job"

    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)
        self.csv_type = self.args["csv_type"].lower()
        self.date_column = self.args.get("date_column")
        self.input_path = self.args["input_path"]

    def run(self):
        self.logger.info("Starting ParquetCollector job...")
        return None

if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'output_path',
        'sns_topic_arn',
        'start_date',
        'end_date',
        'input_path',
        'file_format',
        'date_column',
    ])

    job = ParquetCollector(args)
    job.run_with_exception_handling()
