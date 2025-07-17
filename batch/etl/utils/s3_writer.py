from etl.utils.base_data_writer import BaseDataWriter


class S3Writer(BaseDataWriter):
    """
    Writer for S3
    """

    def __init__(self, output_path, partition_column=None, file_format="parquet"):
        self.output_path = output_path
        self.file_format = file_format
        self.partition_column = partition_column

    def write(self, df, mode="overwrite"):
        if mode not in ["overwrite", "append"]:
            raise ValueError("Mode must be either 'overwrite' or 'append'")

        if self.partition_column:
            df.write.mode(mode).format(self.file_format).partitionBy(
                self.partition_column
            ).save(self.output_path)

        else:
            df.write.mode(mode).format(self.file_format).save(f"{self.output_path}/all")
