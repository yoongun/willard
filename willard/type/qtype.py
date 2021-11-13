from abc import ABCMeta
from willard.type.decorator import subscriptable


@subscriptable
class qtype(metaclass=ABCMeta):
    pass
