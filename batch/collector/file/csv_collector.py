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
        self.date_column = self.args.get("date_column")
        self.partition_key = self.args.get("partition_key")
        self.input_path = self.args["input_path"]

    def run(self):
        self.logger.info("Reading CSV...")
        df = self.spark.read \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .csv(self.input_path)

        if self.partition_key and hasattr(self, 'date_range') and self.date_range:
            # read with partition key filter
            start = self.date_range[0].strftime("%Y-%m-%d")
            end = self.date_range[-1].strftime("%Y-%m-%d")

            self.logger.info(f"Filtering {self.date_column} between {start} and {end}...")
            df = df.filter(
                (col(self.partition_key) >= lit(start)) &
                (col(self.partition_key) <= lit(end))
            )

            if self.date_column:
                # write partition by date column
                self.spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
                df.write \
                    .mode("overwrite") \
                    .partitionBy(f"{self.date_column}") \
                    .parquet(self.output_path)
            else:
                # write all in one file
                df.write \
                .mode("overwrite") \
                .parquet(f"{self.output_path}/all")
                
        else:
            self.logger.info("No date filter applied.")
            df.write \
                .mode("overwrite") \
                .parquet(f"{self.output_path}/all")

        self.logger.info("CsvCollector job completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_path", required=True)

    parser.add_argument("--partition_key", default=None)
    parser.add_argument("--sns_topic_arn", default=None)
    parser.add_argument("--start_date", default=None)
    parser.add_argument("--end_date", default=None)
    parser.add_argument("--date_column", default=None)

    args = parser.parse_args()
    args_dict = vars(args)

    job = CsvCollector(args_dict)
    job.run_with_exception_handling()