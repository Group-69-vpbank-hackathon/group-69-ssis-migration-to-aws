import argparse
from etl.core_modules.base.base_processor import BaseProcessor
from etl.utils.data_writer_factory import create_writer
class Transformer(BaseProcessor):
    JOB_NAME = 'transformer'
    
    def __init__(self, args, data_writer):
        super().__init__(args, self.JOB_NAME, data_writer)
        self.script_file = self.args.get("script_file")
        self.data_sources = self.args.get("data_sources")
        self.temp_views = self.args.get("temp_views")
        self.output_path = self.args.get("output_path")

    def _register_temp_view(self):
        self.logger.info("Register temp views.")
        sources = [s.strip() for s in self.data_sources.split(",")]
        views = [v.strip() for v in self.temp_views.split(",")]

        if len(sources) != len(views):
            raise ValueError("data_sources and temp_views must have the same number of items.")

        for source, view in zip(sources, views):
            self.logger.info(f"Reading {source} as {view}")
            df = self._read(input_path=source)
            df.createOrReplaceTempView(view)
            
    def _execute_query(self):
        self.logger.info(f"Reading SQL script from {self.script_file}")
        with open(self.script_file, "r") as f:
            sql_query = f.read()

        self.logger.info("Executing SQL query...")
        result_df = self.spark.sql(sql_query)
        return result_df
        
    def process(self):
        self._register_temp_view()
        result_df = self._execute_query()
        self.data_writer.write(result_df)

        self.logger.info("Transformation completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--script_file", required=True)
    parser.add_argument("--data_sources", required=True)
    parser.add_argument("--temp_views", required=True)
    parser.add_argument("--data_writer", required=True)
    
    parser.add_argument("--output_path")
    parser.add_argument("--jdbc_url")
    parser.add_argument("--table_name")

    args = parser.parse_args()
    args_dict = vars(args)
    
    data_writer = create_writer(args_dict)

    job = Transformer(args_dict, data_writer)
    job.run()
