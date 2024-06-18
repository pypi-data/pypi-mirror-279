import abc
import typing

T = typing.TypeVar('T')


class BaseFactory(typing.Generic[T], abc.ABC):
    @abc.abstractmethod
    def create(self, model: T) -> T:
        pass
