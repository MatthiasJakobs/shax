from abc import ABC, abstractmethod
from typing import Iterable, Union

# define coalition type
Coalition = Union[int, Iterable[int]]


class BaseValueExtractor(ABC):

    @abstractmethod
    def value(self, S: Coalition) -> float:
        pass

    @abstractmethod
    def n_players(self) -> int:
        pass


class FeatureValueExtractor(BaseValueExtractor):

    def __init__(self, model, X, y):
        self.model = model
        self.X = X
        self.y = y

    def value(self, S: Coalition) -> float:
        return NotImplemented

    def n_players(self) -> int:
        return self.X.shape[-1]

