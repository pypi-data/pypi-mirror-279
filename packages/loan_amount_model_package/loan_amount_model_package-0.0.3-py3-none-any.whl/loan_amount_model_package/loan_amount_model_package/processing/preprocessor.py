from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class Mapper(BaseEstimator, TransformerMixin):
    def __init__(self, variable:list[str], mapping: dict):
        self.mapping = mapping
        self.variable = variable
        super().__init__()

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X):
        X = X.copy()
        for var in self.variable:
            X[var] = X[var].map(self.mapping)
        return X