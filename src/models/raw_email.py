from abc import ABC, abstractmethod


class RawEmail(ABC):
    @abstractmethod
    def source(self):
        pass

    @abstractmethod
    def destinations(self):
        pass

    @abstractmethod
    def raw_message(self):
        pass
