import pandas as pd

from .._tools._utils import binarize_columns, sanity_checker
from ._dataset_metrics import *


class FairnessAnalysis(sanity_checker):
    """The FairnessAnalysis class gives an easy and straightforward way to assess the fairness and the biais of a dataset.

    Parameters
    ----------
    X : pd.DataFrame
        The dataset to analyse, including the target column.
    y : str
        The target column name.
    positive_output_target : Any
        the output considered positive for the given target.
    protected_attributes : list
        List of the protected attributes of the dataset.
    privileged_group : dict
        privileged class for each protected attribute.

    Attributes
    ----------
    **After self.get_disparate_impact_ratio() is called:**
    disparate_impact_ratio : dict
        The Disparate Impact Ratio for each unprivileged class of each protected attribute.
    RMSDIR : dict
        The Root Mean Squared of DIR the classes of each protected attribute.

    **After self.get_statistical_parity_difference() is called:**
    statistical_parity_difference : dict
        The statistical parity difference of each protected attribute.

    **After self.get_pointwise_mutual_information() is called:**
    pointwise_mutual_information : dict
        The pointiwise mutual information between each class of each protected attribute with each output.
    pointwise_mutual_information_ratio : dict
        The PMI of the unprivileged class over the PMI of the privileged class for each output.
    RMSPMI : dict
        The Root Mean Squared of the PMI of the classes of each protected attribute.

    **After self.get_balance() is called:**
    balance : dict(pd.DataFrame)
        The number of element of each class of each protected attribute.
    balance_index : dict
        The balance index of each protected attribute.

    **After self.get_fairness_score() is called:**
    attribute_fairness_score : dict
        The Composite Fairness Score (CFS) for each protected attribute.
    fairness_score : float
        The overall Composite Fairness Score (CFS) of the dataset.
        """

    def __init__(self, X: pd.DataFrame, y: pd.DataFrame, positive_output_target, protected_attributes: list, privileged_groups: dict):
        super()._sanity_check(X, y, positive_output_target,
                              protected_attributes, privileged_groups)

        self.X = X
        self.protected_attributes = protected_attributes
        self.privileged_groups = privileged_groups

        # set y attribute
        self.y = y
        self.positive_output_target = positive_output_target

    def _make_binary_column(self, X: pd.DataFrame, protected_attribute: str, privileged_group: str):
        """Returns a DataFrame which contains of column of the protected attribute with binary value (privileged and non_privileged)
        and a column of the output with binary value (positive output and non_positive output).

        Parameters
        ----------
        X : pd.DataFrame
            The dataset to trandform.
        protected_attributes : str
            The protected attributes you want to binarize.
        privileged_group : str
            The privileged class for the protected attribute

        Returns
        ----------
        [pd.DataFrame] : X with the binarized protected attribute (privileged_group, non_privileged_group)
        """

        return binarize_columns(X, [protected_attribute], {protected_attribute: privileged_group})

    def get_disparate_impact_ratio(self, binary=False):
        """
        The Disparate Impact Ratio (DIR) is the ratio of rate of favorable outcomes
        for the unprivileged group to that of the privileged group.

        Parameters
        ----------
        binary : bool, optional
            True if the protected attribute(s) and output should be binarized. Defaults to False.

        Returns
        ----------
        [dict, dict] : the DIR of each class of each protected attribute and the RMSDIR of each protected attribute
        """

        self.disparate_impact_ratio = {}
        self.RMSDIR = {}
        data = self.X.copy()

        for protected_attribute in self.protected_attributes:
            privileged_group = self.privileged_groups[protected_attribute]
            if binary:
                data = self._make_binary_column(
                    data, protected_attribute, privileged_group)

            dir, RMSDIR_val = DIR(data, self.y,
                                  protected_attribute, privileged_group,
                                  self.positive_output_target
                                  )

            self.disparate_impact_ratio[protected_attribute] = dir
            self.RMSDIR[protected_attribute] = RMSDIR_val

        return self.disparate_impact_ratio, self.RMSDIR

    def get_statistical_parity_difference(self, binary=False):
        """
        The Statistical Parity Difference (SPD) is the difference of the rate of favorable outcomes
        received by the unprivileged group to the privileged group.

        Parameters
        ----------
        binary : bool, optional
            True if the protected attribute(s) and output should be binarized. Defaults to False.

        Returns
        ----------
        [dict]: The statistical parity difference of each protected attribute.
        """

        self.statistical_parity_difference = {}
        data = self.X.copy()
        for protected_attribute in self.protected_attributes:

            privileged_group = self.privileged_groups[protected_attribute]
            if binary:
                data = self._make_binary_column(
                    data, protected_attribute, privileged_group)

            self.statistical_parity_difference[protected_attribute] = SPD(data, self.y,
                                                                          protected_attribute, privileged_group,
                                                                          self.positive_output_target
                                                                          )

        return self.statistical_parity_difference

    def get_pointwise_mutual_information(self, binary=False):
        """The (Normalized) Pointwise Mutual Information is a measure of association. It compares
        the probability of two events happening together to this probability if these events were independents.

        Parameters
        ----------
        binary : bool, optional
            True if the protected attribute(s) and output should be binarized. Defaults to False.

        Returns
        ----------
        [dict, dict, dict] : The pointwise mutual information and pointwise mutual information ratio fo each
        class of each protected attribute ans the RMSPMI for each protected attribute.
        """

        self.pointwise_mutual_information = {}
        self.pointwise_mutual_information_ratio = {}
        self.RMSPMI = {}

        data = self.X.copy()
        for protected_attribute in self.protected_attributes:

            privileged_group = self.privileged_groups[protected_attribute]
            if binary:
                data = self._make_binary_column(
                    data, protected_attribute, privileged_group)

            pmi, pmir, RMSPMI_val = PMI(data, self.y,
                                        protected_attribute, privileged_group,
                                        self.positive_output_target
                                        )

            self.pointwise_mutual_information[protected_attribute] = pmi
            self.pointwise_mutual_information_ratio[protected_attribute] = pmir
            self.RMSPMI[protected_attribute] = RMSPMI_val

        return self.pointwise_mutual_information, self.pointwise_mutual_information_ratio,  self.RMSPMI

    def get_balance(self, binary=False):
        """The balance is the number of element for each class of the protected attributes. It can highlight
        potential biais when training a model. The balance index gives a measure of the balance. 1 means
        that the features are perfectly balanced (all the classes of each feature has the same number of
        element), 0 is the worst case (one class has all the element).

        Parameters
        ----------
        binary : bool, optional
            True if the protected attribute(s) and output should be binarized. Defaults to False.

        Returns
        ----------
        [dict, dict] : the balance and the balance index of each protected_attribute
        """

        self.balance = {}
        self.balance_index = {}
        data = self.X.copy()
        for protected_attribute in self.protected_attributes:

            privileged_group = self.privileged_groups[protected_attribute]
            if binary:
                data = self._make_binary_column(
                    data, protected_attribute, privileged_group)

            self.balance[protected_attribute] = balance(data, self.y,
                                                        protected_attribute, privileged_group,
                                                        self.positive_output_target)

            self.balance_index[protected_attribute] = balance_index(data, self.y,
                                                                    protected_attribute, privileged_group,
                                                                    self.positive_output_target)

        self.average_balance_index = sum(
            self.balance_index.values())/len(self.balance_index)

        return self.balance, self.balance_index

    def get_CBS(self, binary=False):
        """Average of the fairness scores for all prrotected attribute. \n
        1 means the dataset is considered completely fair, 0 not fair at all.

        Parameters
        ----------
        binary : bool, optional
            True if the protected attribute(s) and output should be binarized. Defaults to False.

        Returns
        ----------
        [dict, int] : The fairness score for each protected attribute and the overall fairness score of the dataset.
        """

        final_score = 0
        data = self.X.copy()
        self.attribute_balance_score = {}

        for protected_attribute in self.protected_attributes:
            privileged_group = self.privileged_groups[protected_attribute]
            if binary:
                # data.to_csv(f"./datasets/data_before_{protected_attribute}.csv")
                data = self._make_binary_column(
                    data, protected_attribute, privileged_group)
                # data.to_csv(f"./datasets/data_after_{protected_attribute}.csv")

            score = CBS(data, self.y,
                        protected_attribute, privileged_group,
                        self.positive_output_target)

            self.attribute_balance_score[protected_attribute] = score
            final_score += score

        self.mean_balance_score = final_score/len(self.protected_attributes)

        return self.attribute_balance_score, self.mean_balance_score

    def _print_results(self):

        print('______\n')

        print("BALANCE INDEX")
        for key, val in self.balance_index.items():
            print(key, val)

        print('______\n')

        print("DISPARATE IMPACT RATIO")
        for key, val in self.disparate_impact_ratio.items():
            print(key, val)
        print("RMSDIR")
        for key, val in self.RMSDIR.items():
            print(key, val)

        print('______\n')

        print("POINTWISE MUTUAL INFORMATION")
        for key, val in self.pointwise_mutual_information.items():
            print(key)
            for c, values in val.items():
                print(c, values)
        print("RMSPMI")
        for key, val in self.RMSPMI.items():
            print(key, val)

        print('______\n')

        print("COMPOSITE FAIRNESS SCORE")
        for key, val in self.attribute_balance_score.items():
            print(key, val)

        print('______\n')

    def get_fairness_analysis(self, binary=False, print_results=True):
        """
        evaluate and print the balance index, DIR, SPD, PMI and fairness score of the dataset.
        Does not return them, but they can be access through class attributes.

        Parameters
        ----------
        binary : bool, optional
            True if the protected attribute(s) and output should be binarized. Defaults to False.
        """
        self.get_balance(binary)

        self.get_disparate_impact_ratio(binary)

        self.get_statistical_parity_difference(binary)

        self.get_pointwise_mutual_information(binary)

        self.get_CBS(binary)

        if print_results:
            self._print_results()
