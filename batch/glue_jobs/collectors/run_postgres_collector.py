from collector.db.postgres_collector import PostgresCollector
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--output_path", required=True)
    parser.add_argument("--jdbc_url", required=True)
    parser.add_argument("--table_name", required=True)

    parser.add_argument("--date_column", default=None)
    parser.add_argument("--date_column_type", default=None)
    parser.add_argument("--sns_topic_arn", default=None)
    parser.add_argument("--granularity", default="daily")
    parser.add_argument("--lookback", default=None)
    parser.add_argument("--rolling_window", default=None)
    parser.add_argument("--start_date", default=None)
    parser.add_argument("--end_date", default=None)
    parser.add_argument("--date_format", default=None)
    parser.add_argument("--order_column", default=None)
    parser.add_argument("--secret_name", default=None)
    
    parser.add_argument("--chunk_size", type=int, default=None)
    parser.add_argument("--read_mode", default=None)
    parser.add_argument("--selected_columns", default=None)
    parser.add_argument("--fetch_size", type=int, default=None)
    parser.add_argument("--max_partition", type=int, default=None)

    args, unknown = parser.parse_known_args()
    args_dict = vars(args)

    job = PostgresCollector(args_dict)
    job.run_with_exception_handling()
