from etl.core_modules.loader import Loader
from etl.utils.data_writer_factory import create_writer
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_path")
    parser.add_argument("--data_writer", required=True)

    parser.add_argument("--sns_topic_arn", default=None)
    parser.add_argument("--source_format", default="parquet")
    parser.add_argument("--target_format", default="parquet")
    parser.add_argument("--partition_key", default=None)

    parser.add_argument("--lookback", type=int, default=0)
    parser.add_argument("--rolling_window", type=int, default=0)
    parser.add_argument("--granularity", default="daily")
    parser.add_argument("--start_date", default=None)
    parser.add_argument("--end_date", default=None)
    parser.add_argument("--date_format", default=None)

    parser.add_argument("--partition_column")  # for S3Writer
    parser.add_argument("--primary_key")  # for SQL DB

    parser.add_argument("--jdbc_url")
    parser.add_argument("--table_name")
    parser.add_argument("--batch_size")
    parser.add_argument("--mode")
    parser.add_argument("--target_partitions")
    parser.add_argument("--secret_name")

    args, unknown = parser.parse_known_args()
    args_dict = vars(args)
    data_writer = create_writer(args=args_dict)

    job = Loader(args_dict, data_writer)
    job.run()
