from etl.utils.s3_writer import S3Writer
from etl.utils.postgres_writer import PostgresWriter


def create_writer(args: dict):
    """
    Factory create data writer
    """
    writer = args.get("data_writer")
    if writer == "postgres":
        return PostgresWriter(
            jdbc_url=args.get("jdbc_url"),
            table=args.get("table_name"),
            secret_name=args.get("secret_name"),
            batch_size=int(args.get("batch_size", 1000)),
            target_partitions=int(args.get("target_partitions", 4)),
        )
    elif writer == "s3":
        return S3Writer(
            output_path=args.get("output_path"),
            partition_column=args.get("partition_column", None),
            file_format=args.get("target_format", "parquet"),
        )
    else:
        raise ValueError("Cannot determine writer.")
