import time
import argparse
from collector.core.base_jdbc_collector import BaseDBCollector
from awsglue.utils import getResolvedOptions

class PostgresCollector(BaseDBCollector):
    """PostgresCollector is a subclass of BaseDBCollector for reading data from PostgreSQL databases."""

    JOB_NAME = "postgres_collector_job"

    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)
        self.fetch_size = int(args.get('fetch_size', '10000'))
        self.max_partition = int(args.get('max_partition', '16'))

    def run(self):
        self.read_and_write()

    def read_by_chunks_id(self):
        # Handle empty date_range by creating a single iteration with None date
        date_ranges = self.date_range if self.date_range else [None]
        
        for event_date in date_ranges:
            date_str = event_date.strftime("%Y-%m-%d") if event_date else None
            where_clause = self._build_where_clause(date_str)
            min_max_query = (
                f"SELECT MIN({self.order_column}) as min_id, MAX({self.order_column}) as max_id "
                f"FROM {self.table_name} {where_clause}")           
            
            min_max_df = self.spark.read.format("jdbc") \
                .option("url", self.jdbc_url) \
                .option("query", min_max_query) \
                .option("user", self.username) \
                .option("password", self.password) \
                .option("driver", "org.postgresql.Driver") \
                .load().first()
            min_id = min_max_df['min_id']
            max_id = min_max_df['max_id']

            if min_id is None or max_id is None:
                self.logger.warning(f"No data for {'whole table' if not event_date else f'date {date_str}'}. Skipping.")
                continue

            est_num_partition = max(1, int((max_id - min_id + 1) / self.chunk_size))
            num_partition = min(est_num_partition, self.max_partition)
            self.logger.info(f"Total rows: {max_id - min_id}, numPartitions: {num_partition}")
            start_time = time.time()

            base_query = f"(SELECT {self.selected_columns} FROM {self.table_name} {where_clause}) as base_query"

            df = self.spark.read.format("jdbc") \
                .option("url", self.jdbc_url) \
                .option("dbtable", base_query) \
                .option("user", self.username) \
                .option("password", self.password) \
                .option("partitionColumn", self.order_column) \
                .option("lowerBound", min_id) \
                .option("upperBound", max_id) \
                .option("numPartitions", num_partition) \
                .option("driver", "org.postgresql.Driver") \
                .option("fetchsize", 10000) \
                .load()
            
            self.logger.info(f"Read completed in {time.time() - start_time:.2f}s")
            output_file = self._get_output_path(event_date) if event_date else f"{self.output_path}/all"
            self.write_to_s3(df, output_file=output_file)

    def read_by_chunks_custom(self):
        # Handle empty date_range by creating a single iteration with None date
        date_ranges = self.date_range if self.date_range else [None]
        
        for event_date in date_ranges:
            date_str = event_date.strftime("%Y-%m-%d") if event_date else None
            where_clause = self._build_where_clause(date_str)

            max_query = f"""
                SELECT COUNT(*) as max_rn
                FROM {self.table_name}
                {where_clause}
            """
            max_df = self.spark.read.format("jdbc") \
                .option("url", self.jdbc_url) \
                .option("query", max_query) \
                .option("user", self.username) \
                .option("password", self.password) \
                .option("pushDownPredicate", True) \
                .option("driver", "org.postgresql.Driver") \
                .load().first()
            max_rn = max_df['max_rn']
            
            num_partitions = max(1, int(max_rn / self.chunk_size))
            
            self.logger.info(f"Total rows: {max_rn}, numPartitions: {num_partitions}")

            row_number_query = f"""
                (
                    SELECT {self.selected_columns},
                        ROW_NUMBER() OVER (ORDER BY {self.order_column}) as rn
                    FROM {self.table_name}
                    {where_clause}
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
                .option("driver", "org.postgresql.Driver") \
                .option("pushDownPredicate", True) \
                .option("fetchsize", 10000) \
                .load()

            df = df.drop("rn")

            self.logger.info(f"Read completed in {time.time() - start_time:.2f}s")
            output_file = self._get_output_path(event_date) if event_date else f"{self.output_path}/all"
            self.write_to_s3(df, output_file=output_file)

    def read_full(self):
        # Handle empty date_range by creating a single iteration with None date
        date_ranges = self.date_range if self.date_range else [None]
        
        for event_date in date_ranges:
            date_str = event_date.strftime("%Y-%m-%d") if event_date else None
            where_clause = self._build_where_clause(date_str)
            base_query = f"SELECT {self.selected_columns} FROM {self.table_name} {where_clause}"

            df = self.spark.read.format("jdbc") \
                .option("url", self.jdbc_url) \
                .option("query", base_query) \
                .option("user", self.username) \
                .option("password", self.password) \
                .option("driver", "org.postgresql.Driver") \
                .option("fetchsize", 10000) \
                .load()

            self.logger.info("Read completed for no chunk.")
            output_file = self._get_output_path(event_date) if event_date else f"{self.output_path}/all"
            self.write_to_s3(df, output_file=output_file)

    def _build_where_clause(self, event_date):
        if event_date and self.date_column and self.date_column_type:
            if self.date_column_type.lower() == 'date':
                return f"WHERE DATE({self.date_column}) = '{event_date}'"
            # Added more date_column_type checks if needed here
        return ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--output_path", required=True)
    parser.add_argument("--date_column", required=True)
    parser.add_argument("--jdbc_url", required=True)
    parser.add_argument("--table_name", required=True)

    parser.add_argument("--sns_topic_arn", default=None)
    parser.add_argument("--start_date", default=None)
    parser.add_argument("--end_date", default=None)
    parser.add_argument("--order_column", default=None)
    parser.add_argument("--secret_name", default=None)
    parser.add_argument("--chunk_size", type=int, default=None)
    parser.add_argument("--read_mode", default=None)
    parser.add_argument("--selected_columns", default=None)
    parser.add_argument("--fetch_size", type=int, default=None)
    parser.add_argument("--max_partition", type=int, default=None)

    args = parser.parse_args()

    args_dict = vars(args)

    job = PostgresCollector(args_dict)
    job.run_with_exception_handling()