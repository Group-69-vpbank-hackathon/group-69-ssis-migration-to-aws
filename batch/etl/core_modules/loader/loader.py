import sys
from etl.core_modules.base.base_processor import BaseProcessor
from awsglue.utils import getResolvedOptions

class Loader(BaseProcessor):
    JOB_NAME = 'loader'
    
    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)

    def process(self):
        raise NotImplementedError("Loader must implement process().")

if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'input_path', 'file_format', 'output_path', 'start_date', 'en'
    ])
    job = Loader(args)
    job.run()
