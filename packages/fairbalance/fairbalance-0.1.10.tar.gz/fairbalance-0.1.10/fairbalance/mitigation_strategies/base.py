from pandas import DataFrame
import functools
from sklearn.base import BaseEstimator
from ..processors import RandomOverSamplerProcessor


class BaseMitigationStrategy(BaseEstimator):
    """Base class for the mitigation strategies.

    Warning: This class should not be used directly. Use the derive classes
    instead.
    """

    def __init__(self, processor=RandomOverSamplerProcessor()):
        self.processor = processor

    def fit(self, X, y):
        self._validate_data(X, y)
        return self

    def resample(self,
                 X,
                 y,
                 protected_attributes: list = None,
                 cont_columns: list = None,
                 cat_columns: list = None
                 ):

        # self.fit(X, y)

        df, protected_attribute = self._get_dataframe_and_protected_attribute(
            X, protected_attributes)

        if protected_attribute not in cat_columns:
            cat_columns.append(protected_attribute)

        X_resampled, y_resampled = self._resample_single_attr(
            df, y, protected_attribute, cont_columns, cat_columns)

        X_final = self._get_final_dataframe(
            X_resampled, protected_attributes, protected_attribute)

        return X_final, y_resampled



    def _get_dataframe_and_protected_attribute(self, X, protected_attributes=None):
        """Returns the final dataframe and protected attribute. Used to make the "super attribute" if needed.
        If not needed, returns the original dataset and the single protected attribute.

        Parameters
        ----------
        X : pd.DataFrame
            The dataset to work on.
        protected_attributes : list, optional
            If it contains only one attribute, the dataset and the attribute are returned.
            If it contains more, makes a composite attribute first, then returns the dataset
            and the composite attribute name. Defaults to None.

        Returns
        ----------
            [pd.DataFrame, str]: The final dataset and the protected attribute to work with.
        """
        df = X.copy()
        self.column_order = df.columns.to_list()
        if protected_attributes:
            if len(protected_attributes) > 1:
                return self._make_super_protected(df, protected_attributes)
            return df, protected_attributes[0]
        return df, protected_attributes

    def _get_final_dataframe(self, X, protected_attributes=None, protected_attribute=None):
        """Returns the final dataframe after all processes are done.

        Parameters
        ----------
        X : pd.DataFrame
            The dataset to work on.
        protected_attributes : list, optional
            The list of protected attributes. Default to Nonz
        protected_attribute : str, optional
            The name of the protected attribute used in the process. Defaults to None.

        Returns
        ----------
        [pd.DataFrame] : The processed final dataset.
        """
        if protected_attributes and len(protected_attributes) > 1:
            X = X.drop(columns=[protected_attribute])
        X = X[self.column_order]
        return X

    def _make_super_protected(self, X, protected_attributes):
        """Make a super protected attribute that is the combination of all given protected attributes called "protected_superclass"

        Parameters
        ----------
        dataset : pd.DataFrame
            dataset to mitigate. It can include the target column but it is not necessary.
        protected_attributes : list
            The list of protected attributes to combine into a single "super attribute".

        Returns
        ----------
        [pd.DataFrame, str] : the transformed dataset and the name "super protected" column
        """

        df = X.copy()
        superprotected_column = functools.reduce(
            lambda a, b: a + "_" + b, protected_attributes)
        df[superprotected_column] = ""
        for protected_attribute in protected_attributes:

            df[superprotected_column] += df[protected_attribute].apply(
                str) + "_"

        df[superprotected_column] = df[superprotected_column].apply(
            lambda x: x[:-1])

        return df, superprotected_column

    def _highest_ratio(self, X, y, protected_attribute):
        """Give the highest ratio of positive output on negative output of all the classes of the protected attribute.
        Necessary for balance_output_for_attribute.

        Parameters
        ----------
        X : pd.DataFrame
            dataset to mitigate that does not include the target column.
        y : pd.Series
            the target column.
        protected_attribute : str
            the protected attribute for which to calculate the highest ratio of positive output.

        Returns
        ----------
        [float, str] : the highest ratio and the associated class
        """
        df = X.copy()

        classes = list(df[protected_attribute].unique())
        r_max = 0
        c_max = classes[0]
        df.loc[:, "target"] = y

        for c in classes:
            r = df[df[protected_attribute] == c]["target"].value_counts(
            )[1]/df[df[protected_attribute] == c]["target"].value_counts()[0]
            if r > 1:
                r = 1/r
            if r > r_max:
                r_max = r
                c_max = c
        return r_max, c_max
