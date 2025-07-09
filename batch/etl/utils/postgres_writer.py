from  etl.utils.base_data_writer import BaseDataWriter
import boto3
import json

class PostgresWriter(BaseDataWriter):
    POSTGRES_DRIVER = "org.postgresql.Driver"
    
    def __init__(self, url, table, secret_name, mode = "overwrite"):
        self.jdbc_url = url
        self.table_name = table
        # self.secret = self.get_secret(secret_name)

        # self.username = self.secret['db_username']
        # self.password = self.secret['db_password']
        
        self.username = 'testuser'
        self.password = 'testpass'
        
        self.mode = mode

    def get_secret(self, secret_name):
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    
    def write(self, df):
        
        properties = {
            "user": self.username,
            "password": self.password,
            "driver": self.POSTGRES_DRIVER
        }
        
        df.write \
          .mode(self.mode) \
          .jdbc(url=self.jdbc_url, table=self.table_name, properties=properties)