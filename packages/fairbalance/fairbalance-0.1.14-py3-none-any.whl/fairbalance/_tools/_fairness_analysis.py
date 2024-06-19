import pandas as pd

from ._utils import binarize_columns
from metrics import *
from ._utils import sanity_checker

class FairnessAnalysis(sanity_checker) :
    def __init__(self, dataset: pd.DataFrame, target : str, positive_output_target, protected_attributes: list, privileged_groups: dict) :
        """
        The FairnessAnalysis class gives an easy and straightforward way to assess the fairness and the biais of a dataset.

        Args:
            dataset (pd.DataFrame): The dataset to analyse, including the target column
            target (str): The target column name
            positive_output_target (str | int | float): the output considered positive for the given target
            protected_attributes (list): list of the protected attributes of the dataset
            privileged_group (dict): privileged class for each protected attribute 
        """
        
        super()._sanity_check(dataset, target, positive_output_target, protected_attributes, privileged_groups)
        
        self.dataset = dataset
        self.protected_attributes = protected_attributes
        self.privileged_groups = privileged_groups
        
        #set target attribute
        self.target = self.dataset[[target]]
        self.positive_output_target = positive_output_target
    
  
    def _make_binary_column(self, dataset :pd.DataFrame, protected_attribute: str, privileged_group: str) :
        """
        Returns a DataFrame which contains of column of the protected attribute with binary value (privileged and non_privileged)
        and a column of the output with binary value (positive output and non_positive output)
        
        Args:
            dataset (pd.DataFrame): the dataset to trandform
            protected_attributes (str): protected attributes you want to binarize
            privileged_group (str): privileged class for the protected attribute 

        Returns:
            (pd.DataFrame): dataset with the binarized protected attribute (privileged_group, non_privileged_group)
        """

        return binarize_columns(dataset, [protected_attribute], {protected_attribute: privileged_group})
    
        
    def get_disparate_impact_ratio(self, binary=False) :
        """
        The Disparate Impact Ratio (DIR) is the ratio of rate of favorable outcomes 
        for the unprivileged group to that of the privileged group.
            
        Args:
            binary (bool, optional): True if the protected attribute(s) and output should be binarized. Defaults to False.
        
        Returns:
            ([dict, dict]): the DIR of each class of each protected attribute and the RMSDIR of each protected attribute
        """   

        self.disparate_impact_ratio = {}
        self.RMSDIR = {}
        data = self.dataset.copy()
        
        for protected_attribute in self.protected_attributes :
            privileged_group = self.privileged_groups[protected_attribute]
            if binary :
                data = self._make_binary_column(data, protected_attribute, privileged_group)
            
            
            dir, RMSDIR = DIR(data, 
                              protected_attribute, privileged_group, 
                              self.target.columns[0], self.positive_output_target
                              )
            
            self.disparate_impact_ratio[protected_attribute] = dir
            self.RMSDIR[protected_attribute] = RMSDIR
        
        return self.disparate_impact_ratio[protected_attribute], RMSDIR 
      
    
    def get_statistical_parity_difference(self, binary=False) :
        """
        The Statistical Parity Difference (SPD) is the difference of the rate of favorable outcomes 
        received by the unprivileged group to the privileged group.
            
        Args:
            binary (bool, optional): True if the protected attribute(s) and output should be binarized. Defaults to False.
        
        Returns:
            ([dict]): The statistical parity difference of each protected attribute.
        """
        
        
        self.statistical_parity_difference = {}
        data = self.dataset.copy()
        for protected_attribute in self.protected_attributes :
    
            privileged_group = self.privileged_groups[protected_attribute]
            if binary :
                data = self._make_binary_column(data, protected_attribute, privileged_group)
                   
            self.statistical_parity_difference[protected_attribute] = SPD(data, 
                                                                          protected_attribute, privileged_group, 
                                                                          self.target.columns[0], self.positive_output_target
                                                                          )
        
        return self.statistical_parity_difference
                    
    
    def get_pointwise_mutual_information(self, binary=False) :
        """
        The (Normalized) Pointwise Mutual Information is a measure of association. It compares the probability of two events happening together to this probability
        if these events were independents.
        
        Args:
            binary (bool, optional): True if the protected attribute(s) and output should be binarized. Defaults to False.
        
        Returns:
            ([dict, dict, dict]): The pointwise mutual information and pointwise mutual informaiton ratio fo each class of each protected attribute
            ans the RMSPMI for each protected attribute.
        """


        self.pointwise_mutual_information = {}
        self.pointwise_mutual_information_ratio = {}
        self.RMSPMI = {}
        
        data = self.dataset.copy()
        for protected_attribute in self.protected_attributes :
    
            privileged_group = self.privileged_groups[protected_attribute]
            if binary :
                data = self._make_binary_column(data, protected_attribute, privileged_group)
            
            pmi, pmir, RMSPMI = PMI(data, 
                            protected_attribute, privileged_group, 
                            self.target.columns[0], self.positive_output_target
                            )
            
            self.pointwise_mutual_information[protected_attribute] = pmi
            self.pointwise_mutual_information_ratio[protected_attribute] = pmir
            self.RMSPMI[protected_attribute] = RMSPMI
                                     
        return pmi, pmir, RMSPMI
                
 
    def get_balance(self, binary=False) :
        """
        The balance is the number of element for each class of the protected attributes. It can highlight potential biais when training a model.
        The balance index gives a measure of the balance. 1 means that the features are perfectly balanced (all the classes of each feature has the 
        same number of element), 0 is the worst case (one class has all the element)
            
        Args:
            binary (bool, optional): True if the protected attribute(s) and output should be binarized. Defaults to False.
        
        Returns:
            ([dict, dict]): the balance and the balance index of each protected_attribute
        """

        
        self.balance = {}
        self.balance_index = {}
        data = self.dataset.copy()
        for protected_attribute in self.protected_attributes :
    
            privileged_group = self.privileged_groups[protected_attribute]
            if binary :
                data = self._make_binary_column(data, protected_attribute, privileged_group)
            
            self.balance[protected_attribute] = balance(data, protected_attribute)
            
            self.balance_index[protected_attribute] = balance_index(data, protected_attribute)
                    
        self.average_balance_index = sum(self.balance_index.values())/len(self.balance_index)
        
        return self.balance, self.balance_index
                 
   
    def get_fairness_score(self, binary=False) :
        """
        Average of the fairness scores for all prrotected attribute. \n 
        1 means the dataset is considered completely fair, 0 not fair at all.
        
        Args:
            binary (bool, optional): True if the protected attribute(s) and output should be binarized. Defaults to False.
        
        Returns:
            ([dict, int]): The fairness score for each protected attribute and the fairness score of the dataset.
        """
        
        final_score = 0
        data = self.dataset.copy()
        self.attribute_fairness_score = {}
        
        for protected_attribute in self.protected_attributes :
            privileged_group = self.privileged_groups[protected_attribute]
            if binary :
                # data.to_csv(f"./datasets/data_before_{protected_attribute}.csv")
                data = self._make_binary_column(data, protected_attribute, privileged_group)
                # data.to_csv(f"./datasets/data_after_{protected_attribute}.csv")

            score = FS(data,
                       protected_attribute,
                       privileged_group,
                       self.target.columns[0],
                       self.positive_output_target)
            
            self.attribute_fairness_score[protected_attribute] = score
            final_score += score
        
        self.fairness_score = final_score/len(self.protected_attributes)
        
        return  self.attribute_fairness_score, self.fairness_score
        
        
    
    def get_fairness_analysis(self, binary=False) :
        """
        evaluate and print the balance index, DIR, SPD, PMI and fairness score of the dataset. Does not return them, but they can be access through class attributes.

        Args:
            binary (bool, optional): True if the protected attribute(s) and output should be binarized. Defaults to False.
        """
        self.get_balance(binary)
        
        self.get_disparate_impact_ratio(binary)
        
        self.get_statistical_parity_difference(binary)
        
        self.get_pointwise_mutual_information(binary)
        
        self.get_fairness_score(binary)

