import bitvec
import numpy as np

from .shax import SHAX
from .values import FeatureValueExtractor

if __name__ == '__main__':
    model = None
    X, y = None, None

    shax = SHAX(FeatureValueExtractor(model, X, y))
    shaps, deltas = shax.attribute(return_delta=True)


    
