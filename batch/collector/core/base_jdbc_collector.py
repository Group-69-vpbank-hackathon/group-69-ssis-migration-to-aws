from ..core.base_collector import BaseCollector

class BaseDBCollector(BaseCollector):
    def __init__(self, args, job_name):
        super().__init__(args, job_name)

        self.jdbc_url = args['jdbc_url']
        self.table_name = args['table_name']
        self.secret = self.get_secret(args['secret_name'])

        self.username = self.secret['db_username']
        self.password = self.secret['db_password']

        self.chunk_size = int(args.get('chunk_size', '1000000'))
        self.order_column = args.get('order_column', 'id')
        self.read_mode = args.get('read_mode', 'full').lower()
        self.max_partition = int(args.get('max_partition', '16'))

    def read_and_write(self):
        count_query = self._build_count_query()
        count_df = self.spark.read.format("jdbc") \
            .option("url", self.jdbc_url) \
            .option("query", count_query) \
            .option("user", self.username) \
            .option("password", self.password) \
            .load()

        total_rows = count_df.collect()[0]['total']
        self.logger.info(f"Total rows to process: {total_rows}")
        
        if total_rows <= self.chunk_size:
            self.logger.info("Dataset is small, using full read mode.")
            self.read_full()
        else:
            if self.read_mode == 'chunk_id':
                self.read_by_chunks_id()
            elif self.read_mode == 'chunk_custom':
                self.read_by_chunks_custom(total_rows)
            elif self.read_mode == 'full':
                self.read_full()
            else:
                raise ValueError(f"Unsupported read_mode: {self.read_mode}")
                
    def _build_base_query(self):
        base = f"SELECT * FROM {self.table_name}"
        where = self._build_where_clause()
        return f"{base} {where}"
    
    def _build_count_query(self):
        base = f"SELECT COUNT(1) FROM {self.table_name}"
        where = self._build_where_clause()
        return f"{base} {where}"

    def _build_where_clause(self):
        if self.date_column and self.start_date and self.end_date:
            return f"WHERE {self.date_column} >= '{self.start_date}' AND {self.date_column} <= '{self.end_date}'"
        return ""
    
    def read_by_chunks_id(self):
        raise NotImplementedError("read_by_chunks_id must implement run().")
    
    def read_by_chunks_custom(self, total_rows):
        raise NotImplementedError("read_by_chunks_custom must implement run().")
    
    def read_full(self):
        base_query = self._build_base_query()

        df = self.spark.read.format("jdbc") \
            .option("url", self.jdbc_url) \
            .option("query", base_query) \
            .option("user", self.username) \
            .option("password", self.password) \
            .load()

        self.logger.info("Processing full table read")
        self.write_to_s3(df, partitionKeys=[self.date_column])
