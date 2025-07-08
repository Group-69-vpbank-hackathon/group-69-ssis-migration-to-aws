import sys
from collector.core.base_jdbc_collector import BaseDBCollector
from awsglue.utils import getResolvedOptions

class MySQLCollector(BaseDBCollector):
    """MySQLCollector is a subclass of BaseDBCollector for reading data from MySQL databases."""
    JOB_NAME = "mysql_collector_job"

    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)      
    
    def run(self):
        self.read_and_write()
    
    def read_by_chunks_id(self):
        """Reads data from MySQL in chunks based on an ID column."""
        self.logger.info("MySQL chunk ID reading not implemented.")
        return None

    def read_by_chunks_custom(self, total_rows):
        """Reads data from MySQL in custom chunks."""
        self.logger.info("MySQL custom chunk reading not implemented.")
        return None

    def read_full(self):
        """Reads all data from MySQL."""
        self.logger.info("MySQL full read not implemented.")
        return None
    
if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'output_path', 'sns_topic_arn', 'start_date', 'end_date', 'date_column',
        'jdbc_url', 'table_name', 'order_column','secret_name', 'chunk_size', 'max_partition'
    ])

    job = MySQLCollector(args)
    job.run_with_exception_handling()