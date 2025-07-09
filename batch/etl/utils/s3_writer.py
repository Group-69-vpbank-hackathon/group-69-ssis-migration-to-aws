from  etl.utils.base_data_writer import BaseDataWriter

class S3Writer(BaseDataWriter):
    """
        Writer for S3
    """
    def __init__(self, output_path, partition_column=None, mode = "overwrite", file_format = "parquet"):
        self.output_path = output_path
        self.mode = mode
        self.file_format = file_format
        self.partition_column = partition_column

    def write(self, df):
        print(f"Writing DataFrame to S3 path: {self.output_path} with mode '{self.mode}'")
        
        if self.partition_column:
            df.write \
            .mode(self.mode) \
            .format(self.file_format) \
            .partitionBy(self.partition_column) \
            .save(self.output_path)
            
        else:
            df.write \
            .mode(self.mode) \
            .format(self.file_format) \
            .save(f"{self.output_path}/all")
            
        print("Write to S3 completed.")
