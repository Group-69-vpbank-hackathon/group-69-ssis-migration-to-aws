import sys
import argparse
from etl.core_modules.base.base_processor import BaseProcessor
from etl.utils.data_writer_factory import create_writer


class Loader(BaseProcessor):
    JOB_NAME = 'etl_loader_job'
    
    def __init__(self, args, data_writer):
        super().__init__(args, self.JOB_NAME, data_writer)
        self.partition_key = self.args.get("partition_key")
        self.source_format = self.args.get("source_format")
        self.target_format = self.args.get("target_format")

    def process(self):
        df = self._read(input_path=self.input_path, partition_key=self.partition_key, file_format=self.source_format)
        self._write(df)

