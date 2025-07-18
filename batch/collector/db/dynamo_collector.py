import sys
from awsglue.utils import getResolvedOptions
from datetime import datetime, timedelta
from collector.core.base_nosql_collector import BaseNoSQLCollector


class DynamoCollector(BaseNoSQLCollector):
    """DynamoCollector is a subclass of BaseNoSQLCollector for reading data from DynamoDB and writing to S3."""

    JOB_NAME = "dynamo_collector_job"

    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)

    def run(self):
        """Main execution method"""
        self.logger.info("Run DynamoDB data collection job.")
        return None
