import sys
from ..core.base_nosql_collector import BaseNoSQLCollector
from awsglue.utils import getResolvedOptions

class DynamoCollector(BaseNoSQLCollector):
    JOB_NAME = "dynamo_collector_job"

    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)

    def run(self):
        self.logger.info("DynamoDB collector not yet implemented.")
        
if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'output_path', 'sns_topic_arn', 'start_date', 'end_date', 'chunk_size'
    ])

    job = DynamoCollector(args)
    job.run_with_exception_handling()