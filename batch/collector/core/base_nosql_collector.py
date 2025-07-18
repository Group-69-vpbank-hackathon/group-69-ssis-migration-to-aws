from ..core.base_collector import BaseCollector


class BaseNoSQLCollector(BaseCollector):
    """BaseNoSQLCollector is an abstract class for reading data from NoSQL databases and writing to S3."""

    def __init__(self, args, job_name):
        super().__init__(args, job_name)

    def run(self):
        raise NotImplementedError(
            "Subclasses of BaseNoSQLCollector must implement run()."
        )
