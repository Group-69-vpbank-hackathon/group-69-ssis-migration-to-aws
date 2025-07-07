import sys
from ..core.base_jdbc_collector import BaseDBCollector
from awsglue.utils import getResolvedOptions

class SqlServerCollector(BaseDBCollector):
    JOB_NAME = "sqlserver_collector_job"

    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)

    def run(self):
        self.read_and_write()

    def read_by_chunks_custom(self, total_rows):
        # count_query = self._build_count_query()

        # count_df = self.spark.read.format("jdbc") \
        #     .option("url", self.jdbc_url) \
        #     .option("query", count_query) \
        #     .option("user", self.username) \
        #     .option("password", self.password) \
        #     .load()

        # total_rows = count_df.collect()[0]['total']
        # self.logger.info(f"Total rows to process: {total_rows}")

        for i in range(0, total_rows, self.chunk_size):
            lower = i + 1
            upper = i + self.chunk_size

            chunk_query = f"""
                SELECT * FROM (
                    SELECT *, ROW_NUMBER() OVER (ORDER BY {self.order_column}) as rownum
                    FROM {self.table_name}
                    {self._build_where_clause()}
                ) t
                WHERE rownum BETWEEN {lower} AND {upper}
            """

            df = self.spark.read.format("jdbc") \
                .option("url", self.jdbc_url) \
                .option("query", chunk_query) \
                .option("user", self.username) \
                .option("password", self.password) \
                .load()

            self.logger.info(f"Processing SQL Server chunk rows {lower}-{upper}")
            self.write_to_s3(df, partitionKeys=[self.date_column])
        
    def read_by_chunk_id(self):
        min_max_query = f"SELECT MIN({self.order_column}) as min_id, MAX({self.order_column}) as max_id FROM {self.table_name} {self._build_where_clause()}"

        min_max_df = self.spark.read.format("jdbc") \
            .option("url", self.jdbc_url) \
            .option("query", min_max_query) \
            .option("user", self.username) \
            .option("password", self.password) \
            .load().collect()[0]

        min_id = min_max_df['min_id']
        max_id = min_max_df['max_id']

        self.logger.info(f"Min ID: {min_id}, Max ID: {max_id}")

        for lower in range(min_id, max_id + 1, self.chunk_size):
            upper = lower + self.chunk_size - 1

            chunk_query = f"SELECT * FROM {self.table_name} {self._build_where_clause()} AND {self.order_column} BETWEEN {lower} AND {upper}"

            df = self.spark.read.format("jdbc") \
                .option("url", self.jdbc_url) \
                .option("query", chunk_query) \
                .option("user", self.username) \
                .option("password", self.password) \
                .load()

            self.logger.info(f"Processing SQL Server ID chunk: {lower}-{upper}")
            self.write_to_s3(df, partitionKeys=[self.date_column])

        
if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'output_path', 'sns_topic_arn', 'start_date', 'end_date',
        'jdbc_url', 'table_name', 'order_column', 'secret_name', 'chunk_size'
    ])

    job = SqlServerCollector(args)
    job.run_with_exception_handling()
