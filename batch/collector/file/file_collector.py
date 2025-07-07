import sys
from awsglue.utils import getResolvedOptions

class FileCollector(BaseCollector):
    JOB_NAME = "file_collector_job"

    def __init__(self, args):
        super().__init__(args, self.JOB_NAME)

    def run(self):
        input_path = self.args['input_path']
        file_format = self.args.get('file_format', 'parquet')

        self.logger.info(f"Reading files from: {input_path} as {file_format}")

        # 1. Nếu có start_date và end_date → đọc partition đúng khoảng
        if self.start_date and self.end_date:
            df = self.spark.read.format(file_format) \
                .load(f"{input_path}/date>={self.start_date}/date<={self.end_date}")
        else:
            df = self.spark.read.format(file_format).load(input_path)

        # 2. Thêm bước lọc ở cấp dataframe (phòng khi date không phải partition key)
        filtered_df = df
        if 'date' in df.columns and self.start_date and self.end_date:
            filtered_df = df.filter((df['date'] >= self.start_date) & (df['date'] <= self.end_date))

        self.write_to_s3(filtered_df, partitionKeys=['date'])


if __name__ == "__main__":
    args = getResolvedOptions(sys.argv, [
        'output_path', 'sns_topic_arn', 'start_date', 'end_date',
        'input_path', 'file_format'
    ])

    job = FileCollector(args)
    job.run_with_exception_handling()
