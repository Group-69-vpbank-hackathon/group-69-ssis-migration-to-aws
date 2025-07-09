from  etl.utils.s3_writer import S3Writer
from  etl.utils.postgres_writer import PostgresWriter


def create_writer(args: dict):
    """
    Factory create data writer
    """
    writer = args.get("data_writer")
    if writer == 'postgres':
        return PostgresWriter(
            url=args['jdbc_url'],
            table=args['table_name'],
            secret_name=args.get('secret_name'),
            mode=args.get('write_mode', 'overwrite')
        )
    elif writer == 's3':
        return S3Writer(
            output_path=args['output_path'],
            partition_column=args.get('partition_column', None),
            mode=args.get('write_mode', 'overwrite'),
            file_format=args.get('target_format', 'parquet')
        )
    else:
        raise ValueError("Cannot determine writer.")