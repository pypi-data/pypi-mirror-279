import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from itertools import groupby


class Processor :
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
    
    def dummify(self, dataset: pd.DataFrame, columns: list) :
        for column in columns :
            assert column in dataset.columns, f"feature {column} not in the dataset"
            assert self.prefix_sep not in column, f"""'{self.prefix_sep}' is the prefix separator for the dummifying process, but is in the column name {column}""" 
        
        return pd.get_dummies(data = dataset, columns=columns, prefix_sep=self.prefix_sep, dtype='int')
    
    def encode(self, dataset: pd.DataFrame, columns: list) :
        for feature in columns :
            assert feature in dataset.columns, f"feature {feature} not in the dataset"
            le = LabelEncoder()
            dataset[feature] = le.fit_transform(dataset[feature])
            self.label_encoders[feature] = le
       
        return dataset
            
    def scale(self, dataset: pd.DataFrame, columns: list) :
        for feature in columns :
            assert feature in dataset.columns, f"feature {feature} not in the dataset"
            scaler = StandardScaler()
            dataset[feature] = scaler.fit_transform(dataset[feature].values.reshape(-1, 1))
            self.scalers[feature] = scaler
        
        return dataset
        
    def process(self, dataset: pd.DataFrame, dummify_cols: list = [], 
                scale_cols: list = [], encode_cols: list = []) :
        df = dataset.copy()
        self._get_columns_types(self, df) 

        self.dummify_cols = dummify_cols
        self.scale_cols = scale_cols
        self.encode_cols = encode_cols
        
        #stardard normalization for columns to scale 
        if scale_cols :
            df = self.scale(df, scale_cols)
                
        #one-hot encoding for columns to dummify
        if dummify_cols :
            df = self.dummify(df, dummify_cols)
        
        #label encoding for columns to encode
        if encode_cols :
            df = self.encode(df, encode_cols)
    
        return df
    
    def undummify(self, dataset: pd.DataFrame) :
        undummified = self._undummify_df(dataset)
        for column in self.dummify_cols :
            undummified[column] = undummified[column].astype(self.types[column])
        return  undummified
    
    def unencode(self, dataset: pd.DataFrame) :
        for feature in self.encode_cols :
            le = self.label_encoders[feature]
            dataset[feature] = le.inverse_transform(dataset[feature])
        return dataset
    
    def unscale(self, dataset: pd.DataFrame) :
        for feature in self.scale_cols :
            scaler = self.scalers[feature]
            dataset[feature] = scaler.inverse_transform(dataset[[feature]])
        return dataset
    
    def unprocess(self, dataset: pd.DataFrame) :
        df = dataset.copy()
        
        #remove dummies
        if self.dummify_cols :
            df = self.undummify(df)
        
        #remove encoding
        if self.encode_cols :
            df = self.unencode(df)
        
        #remove scaling
        if self.scale_cols :
            df = self.unscale(df)
            
        return df



    def _undummify_df(self, dataset: pd.DataFrame):
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
