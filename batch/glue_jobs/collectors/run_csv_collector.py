from collector.file.csv_collector import CsvCollector
import argparse

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--input_path", required=True)
    args.add_argument("--output_path", required=True)
    args.add_argument("--partition_key")
    args.add_argument("--sns_topic_arn")
    args.add_argument("--start_date")
    args.add_argument("--end_date")
    args.add_argument("--date_column")
    args.add_argument("--schema_json")
    parsed = vars(args.parse_args())

    job = CsvCollector(parsed)
    job.run_with_exception_handling()
