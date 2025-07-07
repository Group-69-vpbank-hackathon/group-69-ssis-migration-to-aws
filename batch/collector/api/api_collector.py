import sys
import requests
from pyspark.sql import Row
from awsglue.utils import getResolvedOptions
from base_collector import BaseCollector

class APICollector(BaseCollector):
    JOB_NAME = "api_collector_job" 

    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)

    def run(self):
        return None

if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
            'output_path', 'sns_topic_arn', 'start_date', 'end_date', 'secret_name',
            'api_url', 'api_headers', 'input_path', 'file_format'
        ])
    job = APICollector(args)
    job.run_with_exception_handling()
