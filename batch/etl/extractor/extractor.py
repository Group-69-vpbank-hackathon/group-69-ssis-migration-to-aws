import sys
from batch.etl.core.base_processor import BaseProcessor
from awsglue.utils import getResolvedOptions

class Extractor(BaseProcessor):
    JOB_NAME = 'extractor'
    
    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)

    def process(self):
        raise NotImplementedError("Extractor must implement process().")

if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'input_path', 'file_format', 'output_path'
    ])
    job = Extractor(args)
    job.run()
