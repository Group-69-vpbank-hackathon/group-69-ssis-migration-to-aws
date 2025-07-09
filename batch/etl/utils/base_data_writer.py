from abc import ABC, abstractmethod

class BaseDataWriter(ABC):
    @abstractmethod
    def write(self, df):
        pass