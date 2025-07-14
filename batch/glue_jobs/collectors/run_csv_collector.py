from collector.file.csv_collector import CsvCollector
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_path", required=True)
    
    parser.add_argument("--partition_key", default=None)
    parser.add_argument("--sns_topic_arn", default=None)
    parser.add_argument("--lookback", default=None)
    parser.add_argument("--rolling_window", default=None)
    parser.add_argument("--granularity", default="daily")
    parser.add_argument("--start_date", default=None)
    parser.add_argument("--end_date", default=None)
    parser.add_argument("--date_format", default=None)
    parser.add_argument("--date_column", default=None)
    parser.add_argument("--schema_json", default=None)

    args, unknown = parser.parse_known_args()
    args_dict = vars(args)

    job = CsvCollector(args_dict)
    job.run_with_exception_handling()
