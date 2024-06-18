
import pandas as pd
from fairbalance.mitigation_strategies import BalanceOutput, BalanceAttributes, BalanceOutputForAttributes, CompleteBalance
from fairbalance.processors import RandomOverSamplerProcessor, RandomUnderSamplerProcessor
from fairbalance.datasets import load_adult
import pytest


class BaseTest:
    def setUp(self, multi=False):
        data, target, cont, cat = load_adult()

        self.dataset = data
        self.target = target
        self.target = self.target.rename(columns={target.columns[0]: "target"})
        if multi:
            self.protected_attributes = ["race", "sex"]
            self.privileged_groups = {"race": "White", "sex": "male"}

        else:
            self.protected_attributes = ["race"]
            self.privileged_groups = {"race": "White"}
        self.cont_columns = cont
        self.cat_columns = cat

    def _test_same_data_shape(self, X_balanced, y_balanced):
        assert self.dataset.columns.to_list() == X_balanced.columns.to_list()
        assert self.target.columns.to_list() == y_balanced.columns.to_list()

        # assert tha the values inside each columns are the same:
        for column in self.cat_columns:
            assert set(self.dataset[column].unique()) == set(
                X_balanced[column].unique())


class TestBalanceOutput(BaseTest):

    def test_resample(self):
        self.setUp()
        self.mitigator = BalanceOutput(processor=RandomOverSamplerProcessor())
        X_balanced, y_balanced = self.mitigator.resample(
            self.dataset, self.target, self.protected_attributes, self.cont_columns, self.cat_columns)

        self._test_same_data_shape(X_balanced, y_balanced)

        # assert that the output is balanced
        assert y_balanced.value_counts()[0] == y_balanced.value_counts()[1]


class TestBalanceAttributes(BaseTest):

    def test_resample(self):
        self.setUp()
        self.mitigator = BalanceAttributes(
            processor=RandomOverSamplerProcessor())
        X_balanced, y_balanced = self.mitigator.resample(
            self.dataset, self.target, self.protected_attributes, self.cont_columns, self.cat_columns)

        # assert that the transformed dataset has the same shape as the initial one
        self._test_same_data_shape(X_balanced, y_balanced)

        # assert that the output is balanced
        for attribute in self.dataset[self.protected_attributes[0]].unique():
            assert X_balanced[self.protected_attributes[0]].value_counts()[attribute] == X_balanced[self.protected_attributes[0]].value_counts()[
                self.privileged_groups[self.protected_attributes[0]]]


class TestBalanceOutputForAttributes(BaseTest):
    def test_resample(self):
        self.setUp()
        self.mitigator = BalanceOutputForAttributes(
            processor=RandomOverSamplerProcessor())
        X_balanced, y_balanced = self.mitigator.resample(
            self.dataset, self.target, self.protected_attributes, self.cont_columns, self.cat_columns)

        # assert that the transformed dataset has the same shape as the initial one
        self._test_same_data_shape(X_balanced, y_balanced)

        # assert that the output for attributes is balanced
        data_resampled = pd.concat([X_balanced, y_balanced], axis=1)

        data_privi = data_resampled[data_resampled[self.protected_attributes[0]]
                                    == self.privileged_groups[self.protected_attributes[0]]]
        for attribute in self.dataset[self.protected_attributes[0]].unique():
            data_B = data_resampled[data_resampled[self.protected_attributes[0]] == attribute]
            assert (data_privi["target"].value_counts()[0]/data_privi["target"].value_counts()[1]) == pytest.approx(
                (data_B["target"].value_counts()[0]/data_B["target"].value_counts()[1]), rel=1e-1)


class TestCompleteBalanceOneProcessor(BaseTest):
    def test_resample(self):
        # test with one processor
        self.setUp()
        self.mitigator = CompleteBalance(
            processor=RandomOverSamplerProcessor())
        X_balanced, y_balanced = self.mitigator.resample(
            self.dataset, self.target, self.protected_attributes, self.cont_columns, self.cat_columns)

        # assert that the transformed dataset has the same shape as the initial one
        self._test_same_data_shape(X_balanced, y_balanced)

        # assert that everything is balanced
        data_resampled = pd.concat([X_balanced, y_balanced], axis=1)

        data_privi = data_resampled[data_resampled[self.protected_attributes[0]]
                                    == self.privileged_groups[self.protected_attributes[0]]]
        for attribute in self.dataset[self.protected_attributes[0]].unique():
            data_B = data_resampled[data_resampled[self.protected_attributes[0]] == attribute]
            assert (data_privi["target"].value_counts()[0]/data_privi["target"].value_counts()[1]) == pytest.approx(
                (data_B["target"].value_counts()[0]/data_B["target"].value_counts()[1]), rel=1e-1)
            assert X_balanced[self.protected_attributes[0]].value_counts(
            )[self.privileged_groups[self.protected_attributes[0]]] == X_balanced[self.protected_attributes[0]].value_counts()[attribute]


class TestCompleteBalanceTwoProcessor(BaseTest):
    def test_resample(self):
        # test with one processor
        self.setUp()
        self.mitigator = CompleteBalance(processor=RandomOverSamplerProcessor(
        ), second_processor=RandomOverSamplerProcessor())
        X_balanced, y_balanced = self.mitigator.resample(
            self.dataset, self.target, self.protected_attributes, self.cont_columns, self.cat_columns)

        # assert that the transformed dataset has the same shape as the initial one
        self._test_same_data_shape(X_balanced, y_balanced)

        # assert that everything is balanced
        data_resampled = pd.concat([X_balanced, y_balanced], axis=1)

        data_privi = data_resampled[data_resampled[self.protected_attributes[0]]
                                    == self.privileged_groups[self.protected_attributes[0]]]
        for attribute in self.dataset[self.protected_attributes[0]].unique():
            data_B = data_resampled[data_resampled[self.protected_attributes[0]] == attribute]
            assert (data_privi["target"].value_counts()[0]/data_privi["target"].value_counts()[1]) == pytest.approx(
                (data_B["target"].value_counts()[0]/data_B["target"].value_counts()[1]), rel=1e-1)
            assert X_balanced[self.protected_attributes[0]].value_counts(
            )[self.privileged_groups[self.protected_attributes[0]]] == X_balanced[self.protected_attributes[0]].value_counts()[attribute]
