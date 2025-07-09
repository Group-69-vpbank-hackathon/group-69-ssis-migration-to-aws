import sys
from etl.core_modules.base.base_processor import BaseProcessor
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import sum

class QualityChecker(BaseProcessor):
    JOB_NAME = 'etl_quality_checker_job'
    
    def __init__(self, args):
        super().__init__(args, self.JOB_NAME, None)
        self.audit_type = self.args.get('audit_type')
        self.source_column = self.args.get('source_column')
        self.target_column = self.args.get('target_column')
        self.source_pạth = self.args['source_path']
        self.target_path = self.args['target_path']
        self.source_df = None
        self.target_df = None
        self.accepted_accuracy = float(self.args.get('accepted_accuracy', 0.01))  # Default to 1% if not provided

    def load_data(self):
        """Load data from source and target paths."""
        self.source_df = self._read(input_path=self.source_pạth, file_format='parquet')
        self.target_df = self._read(input_path=self.target_path, file_format='parquet')
        
    def check_sum(self):
        """
            Check if the sum of source and target columns are equal in a distributed manner.
        """
        source_sum_df = self.source_df.select(sum(self.source_column).alias("sum_val"))
        target_sum_df = self.target_df.select(sum(self.target_column).alias("sum_val"))

        source_sum = source_sum_df.first()[0]
        target_sum = target_sum_df.first()[0]
        
        source_sum = source_sum or 0
        target_sum = target_sum or 0

        if target_sum == 0:
            is_passed = (source_sum == 0)
        else:
            accuracy = (source_sum - target_sum) / target_sum
            is_passed = abs(accuracy) <= self.accepted_accuracy

        if is_passed:
            self.logger.info(f"Sum check passed: Source sum ({source_sum}) vs Target sum ({target_sum}).")
        else:
            message = f"Sum mismatch: Source sum ({source_sum}) != Target sum ({target_sum})."
            self.logger.error(f"Sum check failed: {message}")
            self.send_notification(f"{self.JOB_NAME} - {message}")
            raise ValueError(message)

    def check_row_quantity(self):
        """
            Check if the number of rows in source and target dataframes are equal.
        """
        source_count = self.source_df.count()
        target_count = self.target_df.count()

        # Logic so sánh (giống như trước)
        if target_count == 0:
            is_passed = (source_count == 0)
        else:
            accuracy = (source_count - target_count) / target_count
            is_passed = abs(accuracy) <= self.accepted_accuracy

        if is_passed:
            self.logger.info(f"Row quantity check passed: {source_count} rows match {target_count} rows.")
        else:
            message = f"Row count mismatch: {source_count} rows do not match {target_count} rows."
            self.logger.error(f"Row quantity check failed: {message}")
            self.send_notification(f"{self.JOB_NAME} - {message}")
            raise ValueError(message)
        
    def process(self):
        """Run the quality check process."""
        self.load_data()
        self.logger.info(f"Loaded source data from {self.source_pạth} and target data from {self.target_path}.")
        
        if self.audit_type == 'summary':
            self.check_sum()
        elif self.audit_type == 'row_quantity':
            self.check_row_quantity()
        else:
            self.logger.error(f"Unsupported audit type: {self.audit_type}")
            self.send_notification(f"{self.JOB_NAME} - Unsupported audit type: {self.audit_type}")
            raise ValueError(f"Unsupported audit type: {self.audit_type}")
