from abc import ABC, abstractmethod, abstractproperty
from functools import cached_property
from typing import Iterable, Optional, Union

import numpy as np


class Coalition:

    def __init__(self, S: Union[int, Iterable[int]], total: Optional[int]=None):
        if isinstance(S, int):
            self.__S = S
            if total is not None:
                assert 1 << total > S, 'coalition has more player indices than `total`'
                self.__n = total
            else:
                self.__n = min(1, S.bit_length())
        elif isinstance(S, Iterable[int]):
            S_, n = 0, 0
            for i in S:
                if i > 0:
                    S_ |= 1
                S_ <<= 1
                n += 1
            self.__S = S_
            self.__n = n

    @property
    def int(self):
        return self.__S
    
    @property
    def bitstring(self):
        return format(self.__S, f'0{self.n_players}b')

    @property
    def bitlist(self):
        l = list(map(int, self.bitstring))
        # reverse, such that l[i] is player [i]
        return l[::-1]
    
    @property
    def bitarray(self):
        return np.asarray(self.list)

    @property
    def indexlist(self):
        return self.indexarray.tolist()

    @property
    def indexset(self):
        return set(self.indexlist)

    @property
    def indexarray(self):
        a, _ = np.where(self.bitarray)
        return a

    @property
    def num_players(self):
        return self.__n


class BaseValueExtractor(ABC):

    @abstractmethod
    def value(self, S: Coalition) -> float:
        pass

    @abstractproperty
    def num_players(self) -> int:
        pass


class FeatureValueExtractor(BaseValueExtractor):

    def __init__(self, model, X, output_fn, **kwargs):
        self.model = model
        self.X = X
        self.output_fn = output_fn
        self.__kwargs = kwargs

    def value(self, S: Coalition) -> float:
        # mask features that are not in coalition S
        # (i.e., set them to zero)
        X_ = self.X * S.bitarray
        # generate model output using masked data
        output = self.model(X_)
        # apply output function
        return self.output_fn(output, **self.__kwargs)

    @property
    def num_players(self) -> int:
        return self.X.shape[-1]

