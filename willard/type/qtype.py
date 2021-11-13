from abc import ABCMeta, abstractmethod
from willard.type.decorator import subscriptable


@subscriptable
class qtype(metaclass=ABCMeta):
    @abstractmethod
    def measure(self):
        raise NotImplementedError(
            "qtype class should implement measure method.")
