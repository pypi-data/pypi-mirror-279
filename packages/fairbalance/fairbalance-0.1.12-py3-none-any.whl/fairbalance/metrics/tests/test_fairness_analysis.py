from fairbalance.tests.base_test import BaseSetUp
from fairbalance.metrics import FairnessAnalysis
from fairbalance.metrics import DIR, SPD, PMI, balance, balance_index, CBS
import pytest


class TestFairnessAnalysis(BaseSetUp):

    def test_init(self):
        self.setUp(multi=True)
        FA = FairnessAnalysis(self.dataset, self.target, 1,
                              self.protected_attributes, self.privileged_groups)
        assert self.dataset.equals(FA.dataset)
        assert self.target.equals(FA.target)
        assert FA.positive_output_target == 1
        assert self.protected_attributes == FA.protected_attributes
        assert self.privileged_groups == FA.privileged_groups

    def test_get_disparate_impact_ratio(self):
        self.setUp(multi=True)
        FA = FairnessAnalysis(self.dataset, self.target, 1,
                              self.protected_attributes, self.privileged_groups)
        DIRs, RMSDIRs = FA.get_disparate_impact_ratio()

        for attribute in self.protected_attributes:
            val, RMSDIR_val = DIR(self.dataset, self.target,
                                  attribute, self.privileged_groups[attribute], 1)
            assert DIRs[attribute] == val
            print(RMSDIRs)
            assert RMSDIRs[attribute] == RMSDIR_val

    def test_get_statistical_parity_difference(self):
        self.setUp(multi=True)
        FA = FairnessAnalysis(self.dataset, self.target, 1,
                              self.protected_attributes, self.privileged_groups)
        SPDs = FA.get_statistical_parity_difference()

        for attribute in self.protected_attributes:
            val = SPD(self.dataset, self.target, attribute,
                      self.privileged_groups[attribute], 1)
            assert SPDs[attribute] == val

    def test_get_pointwise_mutual_information(self):
        self.setUp(multi=True)
        FA = FairnessAnalysis(self.dataset, self.target, 1,
                              self.protected_attributes, self.privileged_groups)
        PMIs, PMIRs, RMSPMIs = FA.get_pointwise_mutual_information()

        for attribute in self.protected_attributes:
            pmi, pmir, rmspmi = PMI(
                self.dataset, self.target, attribute, self.privileged_groups[attribute], 1)
            assert PMIs[attribute] == pmi
            assert PMIRs[attribute] == pmir
            assert RMSPMIs[attribute] == rmspmi

    def test_get_balance(self):
        self.setUp(multi=True)
        FA = FairnessAnalysis(self.dataset, self.target, 1,
                              self.protected_attributes, self.privileged_groups)
        bals, bal_idxs = FA.get_balance()

        for attribute in self.protected_attributes:
            bal = balance(self.dataset, self.target, attribute,
                          self.privileged_groups[attribute], 1)
            bal_idx = balance_index(
                self.dataset, self.target, attribute, self.privileged_groups[attribute], 1)
            assert bals[attribute].equals(bal)
            assert bal_idxs[attribute] == bal_idx

    def test_get_CBS(self):
        self.setUp(multi=True)
        FA = FairnessAnalysis(self.dataset, self.target, 1,
                              self.protected_attributes, self.privileged_groups)
        CBSs, mean_CBS = FA.get_CBS()
        sum_cbs = 0
        for attribute in self.protected_attributes:
            cbs = CBS(self.dataset, self.target, attribute,
                      self.privileged_groups[attribute], 1)
            assert CBSs[attribute] == cbs
            sum_cbs += cbs

        assert mean_CBS == sum_cbs/len(self.protected_attributes)

    def test_get_fairness_analysis(self):
        self.setUp(multi=True)
        FA = FairnessAnalysis(self.dataset, self.target, 1,
                              self.protected_attributes, self.privileged_groups)
        FA.get_fairness_analysis()
