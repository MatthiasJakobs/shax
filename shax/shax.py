from collections import defaultdict
from functools   import lru_cache

from .tools import graycode
from .value import BaseValueExtractor, Coalition


class SHAX:

    def __init__(self, value_extractor: BaseValueExtractor):
        self.value_extractor = value_extractor

    # player_idx list[tuple[int]] | int | tuple[int] | None
    # n_samples: if int: number samples, if float: fraction of 2**n, if none do all
    def attribute(self, players=None, return_delta=False, weight_fn=None, samples=None, workers=1, max_cache_size=None):
        n = self.value_extractor.num_players
        v = lru_cache(maxsize=max_cache_size)(self.value_extractor.value)
        Φ = defaultdict(float)
        i, Si = 0, Coalition(0, total=n)
        vi = v(Si)
        for j in map(graycode, range(1, 1<<n)):
            Sj = Coalition(j, total=n)
            vj = v(Sj)
            Δv = vj - vi       if j > i else vi - vj
            w  = weight_fn(Si) if j > i else weight_fn(Sj)
            Φ[(i^j).bit_length()-1] += w * Δv
            

        return NotImplemented
