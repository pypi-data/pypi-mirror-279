import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from itertools import groupby


class BaseProcessor:
    """Dataset processor to dummify, encode and scale columns and adapt it to learning or mitigation.
    A Processor object shouldn't be used to process different datasets. If you need to process two different datasets,
    it is good practice to use two different processors.

    Parameters
    ----------
    prefix_sex : str, optional
        The prefix separator for dummification and undummification. It shouldn't be in any columns name of the dataset. Default to "~".
    """

    def __init__(self, prefix_sep: str = "~"):
        self.prefix_sep = prefix_sep
        self.scalers = {}
        self.label_encoders = {}
        self.types = {}

    def _get_columns_types(self, dataset: pd.DataFrame):
        self.types = dataset.dtypes

    def _get_columns_order(self, dataset):
        self.columns_order = dataset.columns.to_list()

    def _dummify(self, dataset: pd.DataFrame, columns: list):
        """Dummify the given columns using the prefix separator defined when initializing the Processor object.
        For example, a column "Race" with values "Male" and "Female" and prefix_sep="~" will become two columns
        "Race~Male" and "Race~Female" with values 1 and 0.

        Parameters
        ----------
        dataset : pd.Dataframe
            The dataset to transform
        columns : list
            The columns to dummify

        Returns
        ----------
        [pd.DataFrame] : The dummified dataset
        """
        for column in columns:

            assert column in dataset.columns, f"feature {column} not in the dataset"
            assert self.prefix_sep not in column, f"""'{self.prefix_sep}' is the prefix separator for the dummifying process, and hsouldn't be in the column name {column}"""

        return pd.get_dummies(data=dataset, columns=columns, prefix_sep=self.prefix_sep, dtype='int')

    def _encode(self, X: pd.DataFrame, columns: list):
        """Encode the given columns.
        Encode the different labels of a column to give them Int values. for example, a column "Race" with values
        "Male" and "Female" would be transformed into a column "Race" with values 1 and 2 where 1 encodes "Male" and
        2 encodes "Female".

        Parameters
        ----------
        dataset : pd.Dataframe
            The dataset to transform
        columns : list
            The columns to dummify

        Returns
        ----------
        [pd.DataFrame] : The encoded dataset
        """
        for feature in columns:
            assert feature in X.columns, f"feature {feature} not in the dataset"
            le = LabelEncoder()
            X[feature] = le.fit_transform(X[feature])
            self.label_encoders[feature] = le

        return X

    def _scale(self, X: pd.DataFrame, columns: list):
        """
        Scale the given columns.
        Scales the columns using the skLearn StandardScaler.

        Parameters
        ----------
        dataset : pd.Dataframe
            The dataset to transform
        columns : list
            The columns to dummify

        Returns
        ----------
        [pd.DataFrame] : The scaled dataset
        """
        for feature in columns:
            assert feature in X.columns, f"feature {feature} not in the dataset"
            scaler = MinMaxScaler()
            X[feature] = scaler.fit_transform(X[feature].values.reshape(-1, 1))
            self.scalers[feature] = scaler

        return X

    def dummify_scale_encode(self, X: pd.DataFrame, dummify_cols: list = [],
                             scale_cols: list = [], encode_cols: list = []):
        """
        Process the datasets by dummifying, scaling and encoding the necessary columns.

        Parameters
        ----------
        dataset : pd.DataFrame
            The dataset to transform.
        dummify_cols : list, optional
            The columns to dummifying. Defaults to [].
        scale_cols : list, optional
            he columns to scale. Defaults to [].
        encode_cols : list, optional
            The columns to encode. Defaults to [].

        Returns
        ----------
        [pd.DataFrame] : The transformed dataset.
        """
        df = X.copy()
        self._get_columns_types(df)
        self._get_columns_order(df)
        self.dummify_cols = dummify_cols
        self.scale_cols = scale_cols
        self.encode_cols = encode_cols

        # stardard normalization for columns to scale
        if scale_cols:
            df = self._scale(df, scale_cols)

        # one-hot encoding for columns to dummify
        if dummify_cols:
            df = self._dummify(df, dummify_cols)

        # label encoding for columns to encode
        if encode_cols:
            df = self._encode(df, encode_cols)

        return df

    def _undummify(self, X: pd.DataFrame):
        """Undummify the columns previously dummified.

        Parameters
        ----------
        dataset : pd.DataFrame
            The dataset to transform

        Returns:
        ----------
        [pd.dataFrame] : The transformed dataset
        """
        undummified = self._undummify_df(X)
        for column in self.dummify_cols:
            undummified[column] = undummified[column].astype(
                self.types[column])
        return undummified

    def _unencode(self, X: pd.DataFrame):
        """Unencode the columns previously encoded.

        Parameters
        ----------
        dataset : pd.DataFrame
            The dataset to transform

        Returns
        ----------
        [pd.dataFrame] : The transformed dataset
        """
        for feature in self.encode_cols:
            le = self.label_encoders[feature]
            X[feature] = le.inverse_transform(
                X[feature]).astype(self.types[feature])
        return X

    def _unscale(self, X: pd.DataFrame):
        """Unscale the columns previously scaled.

        Parameters
        ----------
        dataset : pd.DataFrame
            The dataset to transform

        Returns
        ----------
        [pd.dataFrame] : The transformed dataset
        """
        for feature in self.scale_cols:
            scaler = self.scalers[feature]
            X[feature] = scaler.inverse_transform(
                X[[feature]]).astype(self.types[feature])
        return X

    def undo_dummify_scale_encode(self, X: pd.DataFrame):
        """Unprocess all the process made when Processor.process was called.

        Parameters
        ----------
        X : pd.DataFrame
            The dataset to transform.

        Returns
        ----------
        [pd.dataFrame] : The transformed dataset
        """

        df = X.copy()

        # remove dummies
        if self.dummify_cols:
            df = self._undummify(df)

        # remove encoding
        if self.encode_cols:
            df = self._unencode(df)

        # remove scaling
        if self.scale_cols:
            df = self._unscale(df)

        df = df[self.columns_order]
        return df

    def _undummify_df(self, X: pd.DataFrame):
        """
        Undummify a dataset using the self.prefix_sep prefix eparator.

        Parameters
        ----------
        X : pd.DataFrame
            The dataset to transform.

        Returns
        ----------
            [pd.dataFrame] : The transformed dataset
        """
        df = X.copy()

        result_series = {}

        # Find dummy columns and build pairs (category, category_value)
        dummmy_tuples = [(col.split(self.prefix_sep)[0], col)
                         for col in df.columns if self.prefix_sep in col]

        # Find non-dummy columns that do not have a ~
        non_dummy_cols = [
            col for col in df.columns if self.prefix_sep not in col]

        # For each category column group use idxmax to find the value.
        for dummy, cols in groupby(dummmy_tuples, lambda item: item[0]):

            # Select columns for each category
            dummy_df = df[[col[1] for col in cols]]

            # Find max value among columns
            max_columns = dummy_df.idxmax(axis=1)

            # Remove category_ prefix
            result_series[dummy] = max_columns.apply(
                lambda item: item.split(self.prefix_sep)[1])

        # Copy non-dummy columns over.
        for col in non_dummy_cols:
            result_series[col] = df[col]

        # Return dataframe of the resulting series
        return pd.DataFrame(result_series)


class ProcessorMixin:
    def process(self, X, y, dummify_cols=None, scale_cols=None, encode_cols=None):
        processed_X, processed_y = self._process(
            X, y, dummify_cols, scale_cols, encode_cols)
        return processed_X, processed_y

    def unprocess(self, X, y):
        unprocessed_X, unprocessed_y = self._unprocess(X, y)
        return unprocessed_X, unprocessed_y

    def set_categorical_features(self, cat_features):
        self.categorical_features = cat_features
