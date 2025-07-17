from etl.utils.base_data_writer import BaseDataWriter
from etl.utils.secret_manager import get_secret


class PostgresWriter(BaseDataWriter):
    POSTGRES_DRIVER = "org.postgresql.Driver"

    def __init__(
        self, jdbc_url, table, secret_name=None, batch_size=1000, target_partitions=4
    ):
        self.jdbc_url = jdbc_url
        self.table_name = table
        self.batch_size = int(batch_size) if batch_size else batch_size
        self.target_partitions = (
            int(target_partitions) if target_partitions else target_partitions
        )
        self.primary_key = self.args.get("primary_key")

        if secret_name:
            secret = get_secret(secret_name)
            self.username = secret["db_username"]
            self.password = secret["db_password"]

    def write(self, df, mode):
        if mode not in ["overwrite", "append", "upsert"]:
            raise ValueError("Mode must be either 'overwrite' or 'append'")

        current_partitions = df.rdd.getNumPartitions()

        # Repartition hoặc coalesce cho song song
        if current_partitions > self.target_partitions:
            df = df.coalesce(self.target_partitions)
        elif current_partitions < self.target_partitions:
            df = df.repartition(self.target_partitions)

        properties = {
            "user": self.username,
            "password": self.password,
            "driver": self.POSTGRES_DRIVER,
            "batchsize": str(self.batch_size),
        }

        print(f"Writing to table '{self.table_name}' with mode '{mode}'")

        if mode == "upsert":
            if not self.primary_key:
                raise ValueError("Primary key must be provided for upsert mode.")
            self._upsert_filter(df, self.primary_key)
            return

        df.write.mode(mode).jdbc(
            url=self.jdbc_url, table=self.table_name, properties=properties
        )

    def _upsert_filter(self, df_new, primary_key):
        df_existing = self.spark.read.jdbc(
            url=self.jdbc_url,
            table=self.table_name,
            properties={
                "user": self.username,
                "password": self.password,
                "driver": self.POSTGRES_DRIVER,
            },
        )

        df_insert = df_new.join(df_existing, on=primary_key, how="left_anti")
        df_update = df_new.join(df_existing, on=primary_key, how="inner")

        df_insert.write.mode("append").jdbc(
            url=self.jdbc_url, table=self.table_name, properties=self.jdbc_properties()
        )

        # delete existing records having id in df_update
        ids_to_delete = [
            row[primary_key]
            for row in df_update.select(primary_key).distinct().collect()
        ]

        import psycopg2

        conn = psycopg2.connect(
            self.jdbc_url.replace("jdbc:postgresql://", "postgresql://"),
            user=self.username,
            password=self.password,
        )
        cursor = conn.cursor()
        delete_query = f"DELETE FROM {self.table_name} WHERE {primary_key} IN %s"
        cursor.execute(delete_query, (tuple(ids_to_delete),))
        conn.commit()
        cursor.close()
        conn.close()

        # write updated records
        df_update.write.mode("append").jdbc(
            url=self.jdbc_url, table=self.table_name, properties=self.jdbc_properties()
        )
