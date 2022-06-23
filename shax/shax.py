from .values import BaseValueExtractor


class SHAX:

    def __init__(self, value_extractor: BaseValueExtractor):
        return NotImplemented

    # player_idx list[tuple[int]] | int | tuple[int] | None
    # n_samples: if int: number samples, if float: fraction of 2**n, if none do all
    def attribute(self, players=None, return_delta=False, weight_fn=None, samples=100):
        return NotImplemented
 
