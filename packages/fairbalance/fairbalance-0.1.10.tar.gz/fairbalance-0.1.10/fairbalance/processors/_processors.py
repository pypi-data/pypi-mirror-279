from imblearn.over_sampling import RandomOverSampler, SMOTENC
from imblearn.under_sampling import RandomUnderSampler
from .base import BaseProcessor, ProcessorMixin


class RandomOverSamplerProcessor(RandomOverSampler, BaseProcessor, ProcessorMixin):
    """Extension of the RandomOverSampler class by imbalance-learn to fit in the fairbalance framework.
    Formally, it simply adds two functions self._process and self._unprocess used in the mitigation strategy.

    Parameters
    ----------
    prefix_sep : str, optional
        The prefix separator used in the dumlifying process. Passed to the BaseProcessor parent class.
    **kwargs :
        Argument for the imblearn.over_sampling.RandomOverSampler parent class.

    """

    def __init__(self, prefix_sep: str = "~", **kwargs):
        RandomOverSampler.__init__(self, **kwargs)
        BaseProcessor.__init__(self, prefix_sep=prefix_sep)

    def _process(self, X, y, dummify_cols=None, scale_cols=None, encode_cols=None):
        return X, y

    def _unprocess(self, X, y):
        return X, y


class RandomUnderSamplerProcessor(RandomUnderSampler, BaseProcessor, ProcessorMixin):
    """Extension of the RandomUnderSampler class by imbalance-learn to fit in the fairbalance framework.
    Formally, it simply adds two functions self._process and self._unprocess used in the mitigation strategy.

    Parameters
    ----------
    prefix_sep : str, optional
        The prefix separator used in the dumlifying process. Passed to the BaseProcessor parent class.
    **kwargs :
        Argument for the imblearn.under_sampling.RandomUnderSampler parent class.

    """

    def __init__(self, prefix_sep: str = "~", **kwargs):
        RandomUnderSampler.__init__(self, **kwargs)
        BaseProcessor.__init__(self, prefix_sep=prefix_sep)

    def _process(self, X, y, dummify_cols=None, scale_cols=None, encode_cols=None):
        return X, y

    def _unprocess(self, X, y):
        return X, y


class SMOTENCProcessor(SMOTENC, BaseProcessor, ProcessorMixin):
    """Extension of the SMOTENC class by imbalance-learn to fit in the fairbalance framework.
    Formally, it simply adds two functions self._process and self._unprocess used in the mitigation strategy.

    Parameters
    ----------
    prefix_sep : str, optional
        The prefix separator used in the dumlifying process. Passed to the BaseProcessor parent class.
    **kwargs :
        Argument for the imblearn.over_sampling.SMOTENC parent class.

    """

    def __init__(self, prefix_sep: str = "~", **kwargs):
        SMOTENC.__init__(self, categorical_features=[], **kwargs)
        BaseProcessor.__init__(self, prefix_sep=prefix_sep)

    def _process(self, X, y, dummify_cols=None, scale_cols=None, encode_cols=None):
        processed_X = self.dummify_scale_encode(X,
                                                dummify_cols=dummify_cols,
                                                scale_cols=scale_cols,
                                                encode_cols=encode_cols)
        cat_columns_ids = [processed_X.columns.get_loc(
            col) for col in processed_X.columns if col not in scale_cols]
        self.categorical_features = cat_columns_ids
        return processed_X, y

    def _unprocess(self, X, y):
        unprocessed_X = self.undo_dummify_scale_encode(X)
        return unprocessed_X, y
