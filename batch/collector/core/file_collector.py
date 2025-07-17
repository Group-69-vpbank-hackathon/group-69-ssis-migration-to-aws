import sys
from awsglue.utils import getResolvedOptions
from collector.core.base_collector import BaseCollector


class FileCollector(BaseCollector):
    def __init__(self, args, job_name):
        super().__init__(args, job_name)

    def run(self):
        return None
