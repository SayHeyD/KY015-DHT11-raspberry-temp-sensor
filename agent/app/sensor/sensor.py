from abc import ABC, abstractmethod

class ISensor(ABC):
    @property
    @abstractmethod
    def _data(self):
        pass

    @_data.setter
    @abstractmethod
    def _data(self, value):
        pass

    @abstractmethod
    def read(self):
        pass