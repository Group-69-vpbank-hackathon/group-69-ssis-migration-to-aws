import sys
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
        
        start = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        end = datetime.strptime(self.end_date, "%Y-%m-%d").date()


        self.logger.info(f"Filtering date column '{self.date_column}' between {self.start_date} and {self.end_date}...")
        df_filtered = df.filter(
            (to_date(col(self.date_column)) >= lit(start)) &
            (to_date(col(self.date_column)) <= lit(end))
        )

        return df_filtered

    def process_partitioned(self):
        self.logger.info("Processing partitioned CSV by date=YYYY-MM-DD...")
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

        if self.csv_type == "single_file":
            df_filtered = self.read_data_single_file()

            self.logger.info("Adding year/month/day columns from date column...")
            df_final = df_filtered \
                .withColumn("year", col(self.date_column).substr(1, 4).cast("int")) \
                .withColumn("month", col(self.date_column).substr(6, 2).cast("int")) \
                .withColumn("day", col(self.date_column).substr(9, 2).cast("int"))

            df_final.show(10)
            self.logger.info(f"Writing output to {self.output_path} partitioned by year/month/day...")
            df_final.write \
                .mode("overwrite") \
                .partitionBy("year", "month", "day") \
                .parquet(self.output_path)

        elif self.csv_type == "partitioned":
            self.process_partitioned()
        else:
            raise ValueError(f"Unknown csv_type: {self.csv_type}")

        self.logger.info("CsvCollector job completed successfully.")


if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'output_path',
        'sns_topic_arn',
        'start_date',
        'end_date',
        'input_path',
        'file_format',
        'csv_type',
        'date_column',
    ])

    job = CsvCollector(args)
    job.run_with_exception_handling()
