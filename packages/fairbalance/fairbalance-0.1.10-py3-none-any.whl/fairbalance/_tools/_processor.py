import pandas as pd
import imblearn.over_sampling as over_sampling
import imblearn.under_sampling as under_sampling
from sklearn.preprocessing import StandardScaler, LabelEncoder
from itertools import groupby
from ..processors.base import BaseProcessor

class _Processor :
    def __init__(self, prefix_sep: str = "~") :
        """
        Dataset processor to dummify, encode and scale columns and adapt it to learning or mitigation.
        A Processor object shouldn't be used to process different datasets. If you need to process two different datasets, 
        it is good practice to use two different processors.
        
        Args:
            prefix_sex (str, optional) : the prefix separator for dummification and undummification. It shouldn't be in any columns name of the dataset. Default to "~". 
        """

        self.prefix_sep = prefix_sep
        self.scalers = {}
        self.label_encoders = {}
        self.types = {}
    
    def _get_columns_types(self, dataset: pd.DataFrame) :
        self.types = dataset.dtypes
    
    def _dummify(self, dataset: pd.DataFrame, columns: list) :
        """
        Dummify the given columns using the prefix separator defined when initializing the Processor object.
        For example, a column "Race" with values "Male" and "Female" and prefix_sep="~" will become two columns "Race~Male" and "Race~Female" with values 1 and 0.
        
        Args:
            dataset (pd.Dataframe) : The dataset to transform
            columns (list) : The columns to dummify
        
        Returns 
            ([pd.DataFrame]) : The dummified dataset  
        """
        for column in columns :
            assert column in dataset.columns, f"feature {column} not in the dataset"
            assert self.prefix_sep not in column, f"""'{self.prefix_sep}' is the prefix separator for the dummifying process, but is in the column name {column}""" 
        
        return pd.get_dummies(data = dataset, columns=columns, prefix_sep=self.prefix_sep, dtype='int')
    
    def _encode(self, dataset: pd.DataFrame, columns: list) :
        """
        Encode the given columns.
        Encode the different labels of a column to give them Int values. for example, a column "Race" with values "Male" and "Female" would be transformed into 
        a column "Race" with values 1 and 2 where 1 encodes "Male" and 2 encodes "Female".
        
        Args:
            dataset (pd.Dataframe) : The dataset to transform
            columns (list) : The columns to dummify
        
        Returns 
            ([pd.DataFrame]) : The encoded dataset  
        """
        for feature in columns :
            assert feature in dataset.columns, f"feature {feature} not in the dataset"
            le = LabelEncoder()
            dataset[feature] = le.fit_transform(dataset[feature])
            self.label_encoders[feature] = le
       
        return dataset
            
    def _scale(self, dataset: pd.DataFrame, columns: list) :
        """
        Scale the given columns.
        Scales the columns using the skLearn StandardScaler.
        
        Args:
            dataset (pd.Dataframe) : The dataset to transform
            columns (list) : The columns to dummify
        
        Returns 
            ([pd.DataFrame]) : The scaled dataset  
        """
        for feature in columns :
            assert feature in dataset.columns, f"feature {feature} not in the dataset"
            scaler = StandardScaler()
            dataset[feature] = scaler.fit_transform(dataset[feature].values.reshape(-1, 1))
            self.scalers[feature] = scaler
        
        return dataset
        
    def process(self, dataset: pd.DataFrame, dummify_cols: list = [], 
                scale_cols: list = [], encode_cols: list = []) :
        """
        Process the datasets by dummifying, scaling and encoding the necessary columns.

        Args:
            dataset (pd.DataFrame): The dataset to transform.
            dummify_cols (list, optional): The columns to dummifying. Defaults to [].
            scale_cols (list, optional): The columns to scale. Defaults to [].
            encode_cols (list, optional): The columns to encode. Defaults to [].

        Returns:
            ([pd.DataFrame]): The transformed dataset.
        """
        df = dataset.copy()
        self._get_columns_types(df) 

        self.dummify_cols = dummify_cols
        self.scale_cols = scale_cols
        self.encode_cols = encode_cols
        
        #stardard normalization for columns to scale 
        if scale_cols :
            df = self._scale(df, scale_cols)
                
        #one-hot encoding for columns to dummify
        if dummify_cols :
            df = self._dummify(df, dummify_cols)
        
        #label encoding for columns to encode
        if encode_cols :
            df = self._encode(df, encode_cols)
    
        return df
    
    
    def _undummify(self, dataset: pd.DataFrame) :
        """Undummify the columns previously dummified.

        Args:
            dataset (pd.DataFrame): The dataset to transform

        Returns:
            ([pd.dataFrame]): The transformed dataset
        """
        undummified = self._undummify_df(dataset)
        for column in self.dummify_cols :
            undummified[column] = undummified[column].astype(self.types[column])
        return  undummified
    
    def _unencode(self, dataset: pd.DataFrame) :
        """Unencode the columns previously encoded.

        Args:
            dataset (pd.DataFrame): The dataset to transform

        Returns:
            ([pd.dataFrame]): The transformed dataset
        """
        for feature in self.encode_cols :
            le = self.label_encoders[feature]
            dataset[feature] = le.inverse_transform(dataset[feature])
        return dataset
    
    def _unscale(self, dataset: pd.DataFrame) :
        """Unscale the columns previously scaled.

        Args:
            dataset (pd.DataFrame): The dataset to transform

        Returns:
            ([pd.dataFrame]): The transformed dataset
        """
        for feature in self.scale_cols :
            scaler = self.scalers[feature]
            dataset[feature] = scaler.inverse_transform(dataset[[feature]])
        return dataset
    
    def unprocess(self, dataset: pd.DataFrame) :
        """Unprocess all the process made when Processor.process was called.

        Args:
            dataset (pd.DataFrame): The dataset to transform.

        Returns:
            ([pd.dataFrame]): The transformed dataset
        """
        
        df = dataset.copy()
        
        #remove dummies
        if self.dummify_cols :
            df = self._undummify(df)
        
        #remove encoding
        if self.encode_cols :
            df = self._unencode(df)
        
        #remove scaling
        if self.scale_cols :
            df = self._unscale(df)
            
        return df



    def _undummify_df(self, dataset: pd.DataFrame):
        """
        Undummify a dataset using the self.prefix_sep prefix eparator. 

        Args:
            dataset (pd.DataFrame): The dataset to transform.

        Returns:
            ([pd.dataFrame]): The transformed dataset
        """
        df = dataset.copy()
        
        result_series = {}

        # Find dummy columns and build pairs (category, category_value)
        dummmy_tuples = [(col.split(self.prefix_sep)[0],col) for col in df.columns if self.prefix_sep in col]

        # Find non-dummy columns that do not have a ~
        non_dummy_cols = [col for col in df.columns if self.prefix_sep not in col]

        # For each category column group use idxmax to find the value.
        for dummy, cols in groupby(dummmy_tuples, lambda item: item[0]):

            #Select columns for each category
            dummy_df = df[[col[1] for col in cols]]

            # Find max value among columns
            max_columns = dummy_df.idxmax(axis=1)

            # Remove category_ prefix
            result_series[dummy] = max_columns.apply(lambda item: item.split(self.prefix_sep)[1])

        # Copy non-dummy columns over.
        for col in non_dummy_cols:
            result_series[col] = df[col]

        # Return dataframe of the resulting series
        return pd.DataFrame(result_series)




class RandomOverSamplerProcessor(over_sampling.RandomOverSampler, BaseProcessor) :     
    def __init__(self) :
        super().__init__()
    
    def _process(self,X, y, cont_columns, cat_columns) :
        return X, y

    def _unprocess(self,X, y) :
        return X, y

class RandomUnderSamplerProcessor(under_sampling.RandomUnderSampler, BaseProcessor) :
    def __init__(self) :
        super().__init__()
    
    def _process(self,X, y, cont_columns, cat_columns) :
        return X, y

    def _unprocess(self,X, y) :
        return X, y

class SMOTENCProcessor(over_sampling.SMOTENC, BaseProcessor) :
    def __init__(self) :
        super().__init__(categorical_features=[])
        
    def _process(self,X, y, cont_columns, cat_columns) :
        self.processor = _Processor()    
        processed_X = self.processor.process(X, scale_cols=cont_columns, encode_cols=cat_columns)
        cat_columns_ids = [processed_X.columns.get_loc(col_name) for col_name in cat_columns]
        self.categorical_features = cat_columns_ids
        return processed_X, y

    def _unprocess(self,X, y) :
        unprocessed_X = self.processor.unprocess(X)
        return unprocessed_X, y
        


if __name__ == "__main__" :
    data = {
        'feature1': [1, 0, 1, 0, 1],
        'feature2': [5, 6, 7, 8, 9],
        'protected_attribute': ['A', 'B', 'A', 'B', 'A'],
    }
    dataset = pd.DataFrame(data)
    target = pd.Series([1, 0, 1, 0, 1])
    
    ros = RandomOverSamplerProcessor()
    # ros.fit_resample(dataset, target)
    daataset, target = ros._process(dataset, target, ["feature2"], ["feature1", "protected_attribute"])
    dataset, target = ros.fit_resample(dataset, target)
    dataset, target = ros._unprocess(dataset, target)