from abc import ABC, abstractmethod

class BaseDataWriter(ABC):
    spark = None

    @abstractmethod
    def write(self, df, mode):
        pass
          
    def set_spark_session(self, spark):
        self.spark = spark