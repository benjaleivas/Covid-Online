from abc import ABC, abstractmethod

class DataType(ABC):
    @abstractmethod
    def sum_by(self):
        pass 

    @abstractmethod
    def fetch_data(self):
        pass