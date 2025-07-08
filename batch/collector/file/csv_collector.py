import sys
import argparse
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import lit, col, to_date
from datetime import datetime

from collector.core.file_collector import FileCollector

class CsvCollector(FileCollector):
    JOB_NAME = "csv_collector_job"

    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)
        self.csv_type = self.args["csv_type"].lower()
        self.date_column = self.args.get("date_column")
        self.input_path = self.args["input_path"]

    def read_data_single_file(self):
        self.logger.info("Reading single file CSV...")
        df = self.spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(self.input_path)
        
        if self.date_column and hasattr(self, 'date_range') and self.date_range:
            start = self.date_range[0].strftime("%Y-%m-%d")
            end = self.date_range[-1].strftime("%Y-%m-%d")
            
            self.logger.info(f"Filtering date column '{self.date_column}' between {start} and {end}...")
            df = df.filter(
                (to_date(col(self.date_column)) >= lit(start)) &
                (to_date(col(self.date_column)) <= lit(end))
            )
        else:
            self.logger.info("No date filter applied - processing entire file")

        return df

    def process_partitioned(self):
        self.logger.info("Processing partitioned CSV by date=YYYY-MM-DD...")
        
        if not hasattr(self, 'date_range') or not self.date_range:
            self.logger.info("No date range specified - processing all partitions")
            pass

        for event_date in self.date_range:
            partition_path = f"{self.input_path.rstrip('/')}/date={event_date.strftime('%Y-%m-%d')}"
            self.logger.info(f"Reading partition: {partition_path}")

            df = self.spark.read \
                .option("header", "true") \
                .option("inferSchema", "true") \
                .csv(partition_path)

            if df.rdd.isEmpty():
                self.logger.info(f"No data in {partition_path}, skipping.")
                continue

            output_file = self._get_output_path(event_date)
            self.write_to_s3(df, output_file=output_file)

    def run(self):
        self.logger.info("Starting CsvCollector job...")

        if self.csv_type == "all_level":
            df = self.read_data_single_file()

            if self.date_column:
                self.logger.info("Adding year/month/day columns from date column...")
                df = df \
                    .withColumn("year", col(self.date_column).substr(1, 4).cast("int")) \
                    .withColumn("month", col(self.date_column).substr(6, 2).cast("int")) \
                    .withColumn("day", col(self.date_column).substr(9, 2).cast("int"))

            self.logger.info(f"Writing output to {self.output_path}")
            
            if self.date_column:
                df.write \
                    .mode("overwrite") \
                    .partitionBy("year", "month", "day") \
                    .parquet(self.output_path)
            else:
                df.write \
                    .mode("overwrite") \
                    .parquet(self.output_path)

        elif self.csv_type == "partitioned":
            self.process_partitioned()
        else:
            raise ValueError(f"Unknown csv_type: {self.csv_type}")

        self.logger.info("CsvCollector job completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--file_format", required=True)
    parser.add_argument("--csv_type", required=True)

    parser.add_argument("--sns_topic_arn", default=None)
    parser.add_argument("--start_date", default=None)
    parser.add_argument("--end_date", default=None)
    parser.add_argument("--date_column", default=None)

    args = parser.parse_args()

    args_dict = vars(args)

    job = CsvCollector(args_dict)
    job.run_with_exception_handling()