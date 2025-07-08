import sys
from awsglue.utils import getResolvedOptions
from collector.core.base_collector import BaseCollector

class FileCollector(BaseCollector):
    def __init__(self, args, job_name):
        super().__init__(args, job_name)

    def run(self):
        return None


if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'output_path', 'sns_topic_arn', 'start_date', 'end_date',
        'input_path', 'file_format'
    ])

    job = FileCollector(args)
    job.run_with_exception_handling()
