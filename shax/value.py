from abc import ABC, abstractmethod, abstractproperty
from functools import cached_property, reduce
from more_itertools import powerset
from operator import or_
from typing import Iterable, Optional, Union

import numpy as np


class Coalition:

    def __init__(self, S: Union[int, Iterable[int]], total: Optional[int]=None):
        try:
            # interpret as list of indices
            self.__S = reduce(or_, [1<<i for i in S], 0)
        except TypeError:
            # S must be int; interpret as bitmask
            self.__S = S
        self.__n = min(1, self.__S.bit_length()) if total is None else total
        assert 1 << self.__n > self.__S, 'coalition has more than `total` players'

    @classmethod
    def from_bitlist(cls, S: Iterable[int]):
            S_ = int(''.join(map(str, S))[::-1], base=2)
            return cls(S_, len(S))
        

    def containing_coalitions(self):
        """Yields all coalitions containing this coalition as a subset.

        Yields:
            Coalition: Coalition containing this coalition as a subset
        """
        # generate bit masks for all zero positions
        masks = []
        for i in range(self.__n):
            pow_i = 1 << i
            if (self.__S & pow_i) <= 0:
                masks.append(pow_i)
        # apply all combinations of bitmasks to this coalition
        for ms in powerset(masks):
            combo = reduce(or_, ms, 0)
            # yield both the containing coalition as well as the combined bit mask
            yield Coalition(self.__S | combo, total=self.__n), Coalition(combo, total=self.__n)

    def __sub__(self, S):
        ones = (1 << self.__n) - 1
        return Coalition(self.__S & (ones ^ S.__S), total=max(self.__n, S.__n))

    @property
    def int(self):
        return self.__S
    
    @property
    def bitstring(self):
        return format(self.__S, f'0{self.num_players}b')

    @property
    def bitlist(self):
        l = list(map(int, self.bitstring))
        # reverse, such that l[i] is player [i]
        return l[::-1]
    
    @property
    def bitarray(self):
        return np.asarray(self.bitlist)

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

