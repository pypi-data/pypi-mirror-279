
import pandas as pd
from imblearn.over_sampling import RandomOverSampler, SMOTENC
from imblearn.under_sampling import RandomUnderSampler
import functools

from ._processor import SMOTENCProcessor, _Processor

from ._utils import sanity_checker


SAMPLING_FUNCTIONS = ["RandomOverSampler", "SMOTENC", "RandomUnderSampler"]

                
class Mitigator(sanity_checker) :

    def __init__(self, method = "RandomOverSampler") :
        """
        Mitigator implement different types of biais mitigation by resampling.

        Args:
            method (str, optional): resampling methods implemented by imblearn. Possible values are "RandomOverSampler", 
            "SMOTENC" and "RandomUnderSampler".  Defaults to "RandomOverSampler".
        """
        
        self._init_sanity_check(method)
        
        self.method = method
        self.mitigator_function = {
            "RandomOverSampler" : RandomOverSampler,
             "SMOTENC" : SMOTENC,
             "RandomUnderSampler" : RandomUnderSampler
        }
    
    def _init_sanity_check(self, method) :
        assert method in SAMPLING_FUNCTIONS, f"method need to be in {SAMPLING_FUNCTIONS}"

    
    def mitigate(self, mitigation_strategy: str, dataset: pd.DataFrame, target: str, 
                 protected_attributes: list = None, cont_columns: list = None, cat_columns: list = None) :
        """
        Mitigate bias using the given mitigation strategy

        Args:
            mitigation_strategy (str): the mitigation strategy to use. Possible values are "balane_output", "balance_protected_attribute", "balance_output for attribute" and "balance_all". 
            "none" is also implemented for benchmarking consistency and simply return the initial dataset and target. 
            dataset (pd.DataFrame): dataset to mitigate, that includes the target column.
            target (str): the target column name
            protected_attributes (list, optional): The attribute(s) to balance. Only necessary for balance_protected_attribute and balance_output_for_attribute. Defaults to None.
            cont_columns (list, optional): The continuous columns in the dataset. Only Necessary if the sampling strategy is SMOTENC. Defaults to None.
            cat_columns (list, optional): The categorical columns in the dataset. Only Necessary if the sampling strategy is SMOTENC. Defaults to None.

        Raises:
            ValueError: If the mitigation strategy does not exist

        Returns:
            ([pd.DataFrame, pd.DataFrame]): the balanced dataframes for the dataset and the target
        """
        if mitigation_strategy == "balance_output" :
            return self.balance_output(dataset, target, protected_attributes, cont_columns, cat_columns)
        elif mitigation_strategy == "balance_protected_attribute" :
            return self.balance_protected_attribute(dataset, target, protected_attributes, cont_columns, cat_columns)
        elif mitigation_strategy == "balance_output_for_attribute" :
            return self.balance_output_for_attribute(dataset, target, protected_attributes, cont_columns, cat_columns)
        elif mitigation_strategy == "balance_all" :
            return self.balance_all(dataset, target, protected_attributes, cont_columns, cat_columns)
        elif mitigation_strategy == "none" :
            return dataset, target
        else :
            raise ValueError
        
    def balance_output(self, dataset: pd.DataFrame, target: str, protected_attributes: list = None, 
                       cont_columns: list = None, cat_columns: list = None) :
        """
        Balance the output with no regards to the protected attributes.
        
        Args: 
            dataset (pd.DataFrame): dataset to mitigate, that includes the target column.
            target (str): the target column name
            protected_attributes (list, optional): Useless for this mitigation strategy, but implemented for API consistency. Defaults to None.
            cont_columns (list, optional): The continuous columns in the dataset. Only Necessary if the sampling strategy is SMOTENC. Defaults to None.
            cat_columns (list, optional): The categorical columns in the dataset. Only Necessary if the sampling strategy is SMOTENC. Defaults to None.

        Returns:
            ([pd.DataFrame, pd.DataFrame]): the balanced dataframes for the dataset and the target
        """
        super()._sanity_check(dataset, target, protected_attributes=protected_attributes)
        
        #if not RandomOverSampler, need to one-hot encode every categorical
        df = dataset.copy()
        target_df = df[target]
        df = df.drop(columns=target)
        
        
        if protected_attributes and len(protected_attributes) > 1 :
            df, protected_attribute = self._make_super_protected(dataset, protected_attributes)
        
        if self.method in ["SMOTENC"] :
            #process
            processor = _Processor()
            processed_df= processor.process(df, scale_cols=cont_columns, encode_cols=cat_columns)

            # Then resample
            cat_columns_ids = [processed_df.columns.get_loc(col_name) for col_name in cat_columns]
            sampler = self.mitigator_function[self.method](cat_columns_ids)
            X_resampled, y_resampled = sampler.fit_resample(processed_df, target_df)
            
            # Then unprocess it
            df_final = processor.unprocess(X_resampled)
            target_final = y_resampled

        else :
            #just resampler
            sampler = self.mitigator_function[self.method]()
            df_final, target_final = sampler.fit_resample(df, target_df)
        
        if protected_attributes and len(protected_attributes) > 1 :
            df_final = df_final.drop(columns = protected_attribute)
        
        return df_final, target_final
            
    def balance_protected_attribute(self, dataset: pd.DataFrame, target: str, protected_attributes: list, 
                                    cont_columns: list = None, cat_columns: list = None) :
        """
        Balance the classes of a protected attribute with no regards to the output. \n
        Should improve the balance for the protected attribute.
        
        Args: 
            dataset (pd.DataFrame): dataset to mitigate, that includes the target column.
            target (str): the target column name
            protected_attributes (list, optional): The attribute(s) to balance. Defaults to None.
            cont_columns (list, optional): The continuous columns in the dataset. Only Necessary if the sampling strategy is SMOTENC. Defaults to None.
            cat_columns (list, optional): The categorical columns in the dataset. Only Necessary if the sampling strategy is SMOTENC. Defaults to None.

        Returns:
            ([pd.DataFrame, pd.DataFrame]): the balanced dataframes for the dataset and the target
        """
        super()._sanity_check(dataset, target, protected_attributes=protected_attributes)
        df = dataset.copy()
        target_df = df[target]
        df = df.drop(columns=target)

        if len(protected_attributes) > 1 :
            df, protected_attribute = self._make_super_protected(dataset, protected_attributes)
        else :
            protected_attribute = protected_attributes[0]

        if self.method in ["SMOTENC"] :
            #preprocess using the protected attribute as a target
            cont_col_buff = [feature for feature in cont_columns if feature != protected_attribute]
            cat_col_buff = [feature for feature in cat_columns if feature != protected_attribute]
            
            processor = _Processor()
            
            processed_df = processor.process(df, scale_cols=cont_col_buff, encode_cols=(cat_col_buff + [protected_attribute]))

            protected_attribute_column = processed_df[protected_attribute]
            processed_df.drop(columns = [protected_attribute], inplace = True)
            processed_df.loc[:,target] = target_df

            cat_column_buff = cat_col_buff.copy()
            cat_column_buff.append(target)
            cat_column_ids = [processed_df.columns.get_loc(col_name) for col_name in cat_column_buff]

            sampler = self.mitigator_function[self.method](categorical_features=cat_column_ids)

            X_resampled, attribute_resampled = sampler.fit_resample(processed_df, protected_attribute_column)
            X_resampled.loc[:, protected_attribute] = attribute_resampled
           
            df_final = processor.unprocess(X_resampled)
            target_final = df_final[target]
            df_final.drop(columns=[target], inplace=True)

        else : 
            protected_attribute_column = df[protected_attribute]
            df.drop(columns = [protected_attribute], inplace = True)
            df.loc[:,target] = target_df

            sampler = self.mitigator_function[self.method]()
            X_resampled, attribute_resampled = sampler.fit_resample(df, protected_attribute_column)
            
            X_resampled.loc[:, protected_attribute] = attribute_resampled
            target_final = X_resampled[target]
            df_final = X_resampled.drop(columns=[target])
        
        if len(protected_attributes) > 1 :
            df_final = df_final.drop(columns = protected_attribute)    
    
        return df_final, target_final
    
    def balance_output_for_attribute(self, dataset: pd.DataFrame, target: str, protected_attributes: list, 
                                     cont_columns: list = None, cat_columns: list = None) :
        """
        Balance the output of the classes for a given protected attribute. \n
        Should improve the DIR for the protected attribute.
        
        Args: 
            dataset (pd.DataFrame): dataset to mitigate, that includes the target column.
            target (str): the target column name
            protected_attributes (list, optional): The attribute(s) to balance. Defaults to None.
            cont_columns (list, optional): The continuous columns in the dataset. Only Necessary if the sampling strategy is SMOTENC. Defaults to None.
            cat_columns (list, optional): The categorical columns in the dataset. Only Necessary if the sampling strategy is SMOTENC. Defaults to None.

        Returns:
            ([pd.DataFrame, pd.DataFrame]): the balanced dataframes for the dataset and the target
        """

        super()._sanity_check(dataset, target, protected_attributes=protected_attributes)
        df = dataset.copy()

        
        if len(protected_attributes) > 1 :
            df, protected_attribute = self._make_super_protected(dataset, protected_attributes)
        else :
            protected_attribute = protected_attributes[0]
    
        classes = list(df[protected_attribute].unique())
        r, max_class = self._highest_ratio(df, target, classes, protected_attribute)
        
        for c in classes :
            if c != max_class :
                # keep only the rows with given class
                class_df = df[df[protected_attribute] == c]
                class_target = class_df[target]
                class_df = class_df.drop(columns=[target])
            
                # resample the target for this class
                if len(list(class_target.unique())) != 1 :
                    
                    
                    if self.method in ["SMOTENC"] :
                        cont_col_buff = [feature for feature in cont_columns if feature != protected_attribute]
                        cat_col_buff = [feature for feature in cat_columns if feature != protected_attribute]
            
                        #preprocess using the protected attribute as a target
                        processor = _Processor()
                        processed_df = processor.process(class_df, scale_cols=cont_col_buff, encode_cols=(cat_col_buff + [protected_attribute]))

                        cat_columns_ids = [processed_df.columns.get_loc(col_name) for col_name in cat_columns]
                        sampler = SMOTENC(sampling_strategy=r, categorical_features=cat_columns_ids)
                        X_resampled, class_target_resampled = sampler.fit_resample(processed_df, class_target)
                        
                        class_resampled = processor.unprocess(X_resampled)
                        class_resampled.loc[:, target] = class_target_resampled
                                
                    elif self.method in ["RandomOverSampler"] :
                        sampler = RandomOverSampler(sampling_strategy=r)
                        class_resampled, class_target_resampled = sampler.fit_resample(class_df, class_target)
                        class_resampled.loc[:, target] = class_target_resampled
                    
                    elif self.method in ["RandomUnderSampler"] :
                        sampler = RandomUnderSampler(sampling_strategy=r)
                        class_resampled, class_target_resampled = sampler.fit_resample(class_df, class_target)
                        class_resampled.loc[:, target] = class_target_resampled      
                
                else :
                    #if there is only one output for the class, there is no way to resample it
                    class_resampled = class_df.copy()
                    class_resampled.loc[:,target] = class_target
                    
                # append the resampled class in final df
                # (drop the rows with this class first to not duplicated them)
                df = df[df[protected_attribute] != c]
                df = pd.concat([df, class_resampled], ignore_index=True)


        target_df = df[target]
        df.drop(columns=[target], inplace=True)
        
        if len(protected_attributes) > 1 :
            df = df.drop(columns = protected_attribute)
              
        return df, target_df
    
    def balance_all(self, dataset: pd.DataFrame, target: str, protected_attributes: list, 
                    cont_columns: list = None, cat_columns: list = None) :
        """
        First balances the protected attribute(s), and then balance their output. Gives an almost perfectly balanced dataset for the protected attribute(s).

        Args: 
            dataset (pd.DataFrame): dataset to mitigate, that includes the target column.
            target (str): the target column name
            protected_attributes (list, optional): The attribute(s) to balance. Defaults to None.
            cont_columns (list, optional): The continuous columns in the dataset. Only Necessary if the sampling strategy is SMOTENC. Defaults to None.
            cat_columns (list, optional): The categorical columns in the dataset. Only Necessary if the sampling strategy is SMOTENC. Defaults to None.

        Returns:
            ([pd.DataFrame, pd.DataFrame]): the balanced dataframes for the dataset and the target
        """
        df, t = self.balance_protected_attribute(dataset, target, protected_attributes, cont_columns, cat_columns) 
        df.loc[:, target] = t
        df, t = self.balance_output_for_attribute(df, target, protected_attributes, cont_columns, cat_columns)
        
        return df, t    
            
            
    def _highest_ratio(self, dataset: pd.DataFrame, target: str, classes: dict, protected_attribute: str) :
        """
        Give the highest ratio of positive output on negative output of all the classes of the protected attribute. Necessary for balance_output_for_attribute.

        Args:
            dataset (pd.DataFrame): dataset to mitigate, that includes the target column.
            target (str): the target column name
            classes (dict): the classes of the protected attribute
            protected_attribute (str): the protected attribute to calculate the highest ratio for.

        Returns:
            ([float, str]): the highest ratio and the associated class
        """
        
        r_max = 0
        c_max = classes[0]
        for c in classes :
            r = dataset[dataset[protected_attribute] == c][target].value_counts()[1]/dataset[dataset[protected_attribute] == c][target].value_counts()[0]
            if r > 1 :
                r = 1/r
            if r > r_max :
                r_max = r
                c_max = c
        return r_max, c_max
   
   
    def _make_super_protected(self, dataset: pd.DataFrame, protected_attributes: list) :
        """
        Make a super protected attribute that is the combination of all given protected attributes called "protected_superclass"

        Args:
            dataset (pd.DataFrame): dataset to mitigate, that includes the target column.
            protected_attributes (list): protected attributes to combine
            
        Returns:
            ([pd.DataFrame, str]): the transformed dataset and the name "super protected" column
        """

        df = dataset.copy()
        superprotected_column = functools.reduce(lambda a, b : a + "_" + b, protected_attributes)
        df[superprotected_column] = ""
        for protected_attribute in protected_attributes :

            df[superprotected_column] += df[protected_attribute].apply(str)  + "_"
                       
        df[superprotected_column] = df[superprotected_column].apply(lambda x : x[:-1])
        
        
        return df, superprotected_column
