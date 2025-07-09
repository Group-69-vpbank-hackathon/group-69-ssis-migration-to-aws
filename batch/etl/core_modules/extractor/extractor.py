import sys
import argparse
from etl.core_modules.base.base_processor import BaseProcessor
from etl.utils.data_writer_factory import create_writer


class Extractor(BaseProcessor):
    JOB_NAME = 'extractor'
    
    def __init__(self, args, data_writer):
        super().__init__(args, self.JOB_NAME, data_writer)
        self.partition_key = self.args.get("partition_key")
        self.source_format = self.args.get("source_format")
        self.target_format = self.args.get("target_format")

    def process(self):
        df = self._read(input_path=self.input_path, partition_key=self.partition_key, file_format=self.source_format)
        # self._write(df, self.target_format)
        self.data_writer.write(df)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--data_writer", required=True)
    
    parser.add_argument("--sns_topic_arn", default=None)
    parser.add_argument("--source_format", default="parquet")
    parser.add_argument("--target_format", default="parquet")
    parser.add_argument("--partition_key", default=None)
    parser.add_argument("--start_date", default=None)
    parser.add_argument("--end_date", default=None)

    args = parser.parse_args()
    args_dict = vars(args)
    data_writer = create_writer(args=args_dict)
    job = Extractor(args_dict, data_writer)
    job.run()
