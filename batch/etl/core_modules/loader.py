import sys
import argparse
from etl.core_modules.base.base_processor import BaseProcessor
from etl.utils.secret_manager import get_secret


class Loader(BaseProcessor):
    JOB_NAME = 'etl_loader_job'
    
    def __init__(self, args, data_writer):
        super().__init__(args, self.JOB_NAME, data_writer)
        self.partition_key = self.args.get("partition_key")
        self.source_format = self.args.get("source_format")
        self.target_format = self.args.get("target_format")

        self.mode = self.args.get("mode")
        self.jdbc_url = self.args.get("jdbc_url") 
        self.table_name = self.args.get("table")
        self.primary_key = self.args.get("primary_key")
        self.secret_name = self.args.get("secret_name")
        self.secret = get_secret(self.secret_name) if self.secret_name else None
        self.username = self.secret.get("username") if self.secret else None
        self.password = self.secret.get("password") if self.secret else None


    def process(self):
        df = self._read(input_path=self.input_path, partition_key=self.partition_key, file_format=self.source_format)
        if self.mode in ['overwrite', 'append']:
            self._write(df, self.mode)
        if self.mode == 'upsert':
            self._upsert_using_anti_join(df, self.primary_key)

    def _upsert_using_anti_join(self, df_new, primary_key):
        df_existing = self.spark.read.jdbc(
            url=self.jdbc_url,
            table=self.table_name,
            properties={
                "user": self.username,
                "password": self.password,
                "driver": self.POSTGRES_DRIVER
            }
        )

        # Insert mới
        df_insert = df_new.join(df_existing, on=primary_key, how="left_anti")

        # Update: xóa phần đã có rồi chèn lại
        df_update = df_new.join(df_existing, on=primary_key, how="inner")

        # Ghi insert
        df_insert.write.mode("append").jdbc(
            url=self.jdbc_url,
            table=self.table_name,
            properties=self.jdbc_properties()
        )

        # Xóa bản ghi cũ có id giống update
        ids_to_delete = [row[primary_key] for row in df_update.select(primary_key).distinct().collect()]
        
        import psycopg2
        conn = psycopg2.connect(self.jdbc_url.replace("jdbc:postgresql://", "postgresql://"),
                                user=self.username,
                                password=self.password)
        cursor = conn.cursor()
        delete_query = f"DELETE FROM {self.table_name} WHERE {primary_key} IN %s"
        cursor.execute(delete_query, (tuple(ids_to_delete),))
        conn.commit()
        cursor.close()
        conn.close()

        # Ghi lại bản ghi mới đã cập nhật
        df_update.write.mode("append").jdbc(
            url=self.jdbc_url,
            table=self.table_name,
            properties=self.jdbc_properties()
        )


    


