from ..core.base_collector import BaseCollector

class BaseDBCollector(BaseCollector):
    """BaseDBCollector is an abstract class for reading data from relational databases and writing to S3."""

    def __init__(self, args, job_name):
        super().__init__(args, job_name)

        self.jdbc_url = args['jdbc_url']
        self.table_name = args['table_name']
        self.selected_columns = args.get('selected_columns', '*').lower()
        # self.secret = self.get_secret(args['secret_name'])

        # self.username = self.secret['db_username']
        # self.password = self.secret['db_password']
        
        self.username = 'testuser'
        self.password = 'testpass'

        self.chunk_size = int(args.get('chunk_size', '1000000'))
        self.order_column = args.get('order_column', 'id')
        self.read_mode = args.get('read_mode', 'full').lower()
        self.max_partition = int(args.get('max_partition', '16'))

    def read_and_write(self):
        self.logger.info(f"Reading data from {self.table_name} in {self.read_mode} mode.")
        if self.read_mode == 'chunk_id':
            self.read_by_chunks_id()
        elif self.read_mode == 'chunk_custom':
            self.read_by_chunks_custom()
        elif self.read_mode == 'full':
            self.read_full()
        else:
            raise ValueError(f"Unsupported read_mode: {self.read_mode}")
    
    def read_by_chunks_id(self):
        raise NotImplementedError("read_by_chunks_id must implement run().")
    
    def read_by_chunks_custom(self):
        raise NotImplementedError("read_by_chunks_custom must implement run().")
    
    def read_full(self):
        raise NotImplementedError("read_full must implement run().")
    


