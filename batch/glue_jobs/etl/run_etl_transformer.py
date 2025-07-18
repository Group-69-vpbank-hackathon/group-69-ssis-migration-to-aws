from etl.core_modules.transformer import Transformer
from etl.utils.data_writer_factory import create_writer
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--script_file", required=True)
    parser.add_argument("--data_sources", required=True)
    parser.add_argument("--temp_views", required=True)
    parser.add_argument("--data_writer", required=True)

    parser.add_argument("--sns_topic_arn", default=None)
    parser.add_argument("--output_path")

    parser.add_argument("--jdbc_url")
    parser.add_argument("--table_name")
    parser.add_argument("--batch_size")
    parser.add_argument("--mode")
    parser.add_argument("--target_partitions")
    parser.add_argument("--secret_name")

    parser.add_argument("--start_date", default=None)
    parser.add_argument("--end_date", default=None)
    parser.add_argument("--lookback", type=int, default=0)
    parser.add_argument("--rolling_window", type=int, default=0)
    parser.add_argument("--granularity", default="daily")

    parser.add_argument("--partition_column")  # for S3Writer
    parser.add_argument("--primary_key")  # for SQL DB

    args, unknown = parser.parse_known_args()
    args_dict = vars(args)

    data_writer = create_writer(args_dict)

    job = Transformer(args_dict, data_writer)
    job.run()
