import sys
from batch.etl.core.base_processor import BaseProcessor
from awsglue.utils import getResolvedOptions

class QualityChecker(BaseProcessor):
    JOB_NAME = 'quality_checker'
    
    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)

    def process(self):
        raise NotImplementedError("QualityChecker must implement process().")
    
if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'input_path', 'file_format'
    ])
    job = QualityChecker(args)
    job.run()
