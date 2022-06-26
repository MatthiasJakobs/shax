from collections import defaultdict
from functools   import lru_cache

from .tools import graycode
from .value import BaseValueExtractor, Coalition


class SHAX:

    def __init__(self, value_extractor: BaseValueExtractor):
        self.value_extractor = value_extractor

    # player_idx list[tuple[int]] | int | tuple[int] | None
    # n_samples: if int: number samples, if float: fraction of 2**n, if none do all
    def attribute(self, players=None, weight_fn=None, samples=None, return_delta=False, workers=1, max_cache_size=None):
        if isinstance(players, int):
            players = [(players,)]
        elif isinstance(players, tuple[int]):
            players = [players]
      
        if samples is None: 
            if players is None:
                return __attribute_all_exact(weight_fn, workers, max_cache_size)
            else:
                return __attribute_exact(players, weight_fn, workers, max_cache_size)
        else:
            # TODO 


    def __attribute_exact(self, players, weight_fn, workers, max_cache_size):
        n = self.value_extractor.num_players
        v = lru_cache(maxsize=max_cache_size)(self.value_extractor.value)
        Φ = defaultdict(float)
        for indices in sorted({ sorted(ixs) for ixs in players }, key=len):
            S = Coalition(indices, total=n)
            for S1, S2 in S.containing_coalitions():
                Δv = v(S1) - v(S2)
                w  = weight_fn(S2, *indices)
                Φ[indices] += w * Δv
        return Φ

    def __attribute_all_exact(self, weight_fn, workers, max_cache_size):
        n = self.value_extractor.num_players
        v = lru_cache(maxsize=max_cache_size)(self.value_extractor.value)
        Φ = defaultdict(float)
        i, Si = 0, Coalition(0, total=n)
        vi = v(Si)
        for j in map(graycode, range(1, 1<<n)):
            Sj = Coalition(j, total=n)
            vj = v(Sj)
            # gray code always produces a single bit at index k:
            k  = (i ^ j).bit_length() - 1
            if i < j:
                Δv = vi - vj
                w  = weight_fn(Sj, k)
            else:
                Δv = vj - vi
                w  = weight_fn(Si, k)
            Φ[(k,)] += w * Δv
            i, Si = j, Sj
        
