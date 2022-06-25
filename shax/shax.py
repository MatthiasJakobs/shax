from functools import lru_cache

from .value import BaseValueExtractor


class SHAX:

    def __init__(self, value_extractor: BaseValueExtractor):
        self.value_extractor = value_extractor

    # player_idx list[tuple[int]] | int | tuple[int] | None
    # n_samples: if int: number samples, if float: fraction of 2**n, if none do all
    def attribute(self, players=None, return_delta=False, weight_fn=None, samples=None, workers=1):

        v = lru_cache()(self.value_extractor.value)
        # TODO
        return NotImplemented