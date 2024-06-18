from fairbalance.tests.base_test import BaseSetUp
from fairbalance.mitigation_strategies import BalanceAttributes
from fairbalance.processors import RandomOverSamplerProcessor
from fairbalance.utils import balanced_train_test_split
import pytest


class TestBalancedTrainTestSplit(BaseSetUp):

    def _test_same_columns(self, X_train, X_test):
        assert X_train.columns.to_list() == X_test.columns.to_list()

    def test_balanced_train_test_split_no_protected_attr(self):
        self.setUp()
        self.mitigator = BalanceAttributes(
            processor=RandomOverSamplerProcessor())

        # test that it makes a train test split
        X_train, X_test, y_train, y_test = balanced_train_test_split(
            self.dataset, self.target)
        self._test_same_columns(X_train, X_test)

    def test_balanced_train_test_split_single_protected_attr(self):
        self.setUp()
        # test that it makes a balanced train test split
        X_train, X_test, y_train, y_test = balanced_train_test_split(
            self.dataset, self.target, self.protected_attributes)
        self._test_same_columns(X_train, X_test)

        # balanced train test split should keep all the elements in train and test
        assert set(X_train[self.protected_attributes[0]].unique()) == set(
            X_test[self.protected_attributes[0]].unique())

        # assert that the classes have the same distribution
        for class_ in X_train[self.protected_attributes[0]].unique():
            assert X_train[X_train[self.protected_attributes[0]] == class_].shape[0] / X_train.shape[0] == pytest.approx(
                X_test[X_test[self.protected_attributes[0]] == class_].shape[0] / X_test.shape[0], rel=1e-0)

        # test that it resamples the training data
        self.mitigator = BalanceAttributes(
            processor=RandomOverSamplerProcessor())
        X_train, X_test, y_train, y_test = balanced_train_test_split(
            self.dataset, self.target, self.protected_attributes, self.mitigator, self.cont_columns, self.cat_columns)
        self._test_same_columns(X_train, X_test)

        for attribute in self.dataset[self.protected_attributes[0]].unique():
            assert X_train[self.protected_attributes[0]].value_counts()[attribute] == X_train[self.protected_attributes[0]].value_counts()[
                self.privileged_groups[self.protected_attributes[0]]]

    def test_balanced_train_test_split_multi_protected_attr(self):
        self.setUp(multi=True)

        X_train, X_test, y_train, y_test = balanced_train_test_split(
            self.dataset, self.target, self.protected_attributes)
        self._test_same_columns(X_train, X_test)

        # balanced train test split should keep all the elements in train and test
        assert set(X_train[self.protected_attributes[0]].unique()) == set(
            X_test[self.protected_attributes[0]].unique())
        assert set(X_train[self.protected_attributes[1]].unique()) == set(
            X_test[self.protected_attributes[1]].unique())

        # test that it resamples the training data
        self.mitigator = BalanceAttributes(
            processor=RandomOverSamplerProcessor())
        X_train, X_test, y_train, y_test = balanced_train_test_split(
            self.dataset, self.target, self.protected_attributes, self.mitigator, self.cont_columns, self.cat_columns)
        self._test_same_columns(X_train, X_test)

        for attribute in self.dataset[self.protected_attributes[0]].unique():
            assert X_train[self.protected_attributes[0]].value_counts()[attribute] == X_train[self.protected_attributes[0]].value_counts()[
                self.privileged_groups[self.protected_attributes[0]]]
        for attribute in self.dataset[self.protected_attributes[1]].unique():
            assert X_train[self.protected_attributes[1]].value_counts()[attribute] == X_train[self.protected_attributes[1]].value_counts()[
                self.privileged_groups[self.protected_attributes[1]]]
