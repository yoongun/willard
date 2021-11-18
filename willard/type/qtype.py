from abc import ABCMeta, abstractmethod
from willard.type.decorator import subscriptable, default_as_select_all


@subscriptable
@default_as_select_all
class qtype(metaclass=ABCMeta):
    @abstractmethod
    def measure(self):
        raise NotImplementedError(
            "qtype class should implement measure method.")

    @property
    def global_state(self):
        return self.qr.state
