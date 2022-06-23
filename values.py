class BaseValueExtractor:

    def value_fn(self, S):
        pass

    def nr_players(self):
        pass

class FeatureValueExtractor(BaseValueExtractor):

    def __init__(self, model, X, y):
        self.model = model
        self.X = X
        self.y = y

    def nr_players(self):
        return self.X.shape[-1]

    def value_fn(self, S):
        return super().value_fn()
