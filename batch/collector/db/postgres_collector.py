import sys
import time
from collector.core.base_jdbc_collector import BaseDBCollector
from awsglue.utils import getResolvedOptions

class PostgresCollector(BaseDBCollector):
    JOB_NAME = "postgres_collector_job"

    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)
        self.username = 'testuser'
        self.password = 'testpass'

    def run(self):
        self.read_and_write()

    def read_by_chunks_id(self):
        min_max_query = f"SELECT MIN({self.order_column}) as min_id, MAX({self.order_column}) as max_id FROM {self.table_name} {self._build_where_clause()}"
        min_max_df = self.spark.read.format("jdbc") \
            .option("url", self.jdbc_url) \
            .option("query", min_max_query) \
            .option("user", self.username) \
            .option("password", self.password) \
            .load().first()
        min_id = min_max_df['min_id']
        max_id = min_max_df['max_id']
        self.logger.info(f"Min ID: {min_id}, Max ID: {max_id}")
        est_num_partition = max(1, int((max_id - min_id + 1) / self.chunk_size))
        num_partition = min(est_num_partition, self.max_partition)
        start_time = time.time()
        df = self.spark.read.format("jdbc") \
            .option("url", self.jdbc_url) \
            .option("dbtable", self.table_name) \
            .option("user", self.username) \
            .option("password", self.password) \
            .option("partitionColumn", self.order_column) \
            .option("lowerBound", min_id) \
            .option("upperBound", max_id) \
            .option("numPartitions", num_partition) \
            .load()
        self.logger.info(f"Read all partitions in parallel, time: {time.time() - start_time:.2f}s")
        partition_keys = [self.date_column] if self.date_column and self.date_column in df.columns else []
        self.write_to_s3(df, partitionKeys=partition_keys)

    def read_by_chunks_custom(self, chunk_size=5000000):
        for event_date in self.date_range:
            max_query = f"""
                SELECT COUNT(*) as max_rn
                FROM {self.table_name}
                {self._build_where_clause(event_date.strftime("%Y-%m-%d"))}
            """
            max_df = self.spark.read.format("jdbc") \
                .option("url", self.jdbc_url) \
                .option("query", max_query) \
                .option("user", self.username) \
                .option("password", self.password) \
                .load().first()
            max_rn = max_df['max_rn']
            
            num_partitions = max(1, int(max_rn / chunk_size))
            
            self.logger.info(f"Total rows: {max_rn}, numPartitions: {num_partitions}")

            row_number_query = f"""
                (
                    SELECT *,
                        ROW_NUMBER() OVER (ORDER BY {self.order_column}) as rn
                    FROM {self.table_name}
                    {self._build_where_clause(event_date.strftime("%Y-%m-%d"))}
                ) AS subq
            """
            
            start_time = time.time()
            df = self.spark.read.format("jdbc") \
                .option("url", self.jdbc_url) \
                .option("dbtable", row_number_query) \
                .option("partitionColumn", "rn") \
                .option("lowerBound", 1) \
                .option("upperBound", max_rn) \
                .option("numPartitions", num_partitions) \
                .option("user", self.username) \
                .option("password", self.password) \
                .load()
            self.logger.info(f"Read completed in {time.time() - start_time:.2f}s")
            output_file = self.output_path + '/year=' + event_date.year + '/month=' + event_date.month + '/day=' + event_date.day
            self.write_to_s3(df, output_file)


if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'output_path', 'sns_topic_arn', 'start_date', 'end_date', 'date_column',
        'jdbc_url', 'table_name', 'order_column', 'secret_name', 'chunk_size'
    ])
    job = PostgresCollector(args)
    job.run_with_exception_handling()
