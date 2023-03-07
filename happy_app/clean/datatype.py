# Jack 
from abc import ABC, abstractmethod

class DataType(ABC):
    '''
    Abstract class for the data structures used throughout the project.
    Contains methods to sum data, pull data from its online source, export
    it to the data folder, and split data collected from multiple years into 
    yearly dataframes. 
    '''
    @abstractmethod
    def sum_by(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def export(self):
        pass

    @abstractmethod
    def split_by_year(self):
        pass
