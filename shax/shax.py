from .values import BaseValueExtractor

class SHAX:

    def __init__(self, value_extractor: BaseValueExtractor):
        pass

    # player_idx list[tuple[int]] | int | tuple[int] | None
    # n_samples: if int: number samples, if float: fraction of 2**n, if none do all
    def attribute(self, player_idx  = None, return_delta: bool = False, weight_fn=None, n_samples=100):
        pass
 
