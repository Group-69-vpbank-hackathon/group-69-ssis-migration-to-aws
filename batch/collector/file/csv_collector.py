import sys
import argparse
import json
from pyspark.sql.types import StructType
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
        self.schema_json = self.args.get("schema_json")

    def run(self):
        self.logger.info(f"Reading CSV from {self.input_path}")

        reader = self.spark.read.option("header", "true")

        if self.schema_json:
            self.logger.info("Using provided schema")
            schema_dict = json.loads(self.schema_json)
            schema = StructType.fromJson(schema_dict)
            df = reader.schema(schema).csv(self.input_path)
        else:
            self.logger.info("Inferring schema")
            df = reader.option("inferSchema", "true").csv(self.input_path)

        if self.partition_key and hasattr(self, "date_range") and self.date_range:
            start = self.date_range[0].strftime("%Y-%m-%d")
            end = self.date_range[-1].strftime("%Y-%m-%d")

            self.logger.info(
                f"Filtering {self.partition_key} between {start} and {end}"
            )
            df = df.filter(
                (col(self.partition_key) >= lit(start))
                & (col(self.partition_key) <= lit(end))
            )

            if self.date_column:
                self.spark.conf.set(
                    "spark.sql.sources.partitionOverwriteMode", "dynamic"
                )
                df.write.mode("overwrite").partitionBy(f"{self.date_column}").parquet(
                    self.output_path
                )
            else:
                df.write.mode("overwrite").parquet(f"{self.output_path}/all")

        else:
            self.logger.info("No date filter applied.")
            df.write.mode("overwrite").parquet(f"{self.output_path}/all")

        self.logger.info("Csv Collector job completed successfully.")
