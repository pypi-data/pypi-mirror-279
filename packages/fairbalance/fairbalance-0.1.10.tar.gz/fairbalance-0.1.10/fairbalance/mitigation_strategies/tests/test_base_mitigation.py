from fairbalance.mitigation_strategies.base import BaseMitigationStrategy
from fairbalance.tests.base_test import BaseSetUp


class TestBaseMitigationStrategy(BaseSetUp):

    def test_get_dataframe_and_protected_attribute(self):
        # test if no protected attribute
        self.setUp()
        baseMitigator = BaseMitigationStrategy()
        df, protected_attribute = baseMitigator._get_dataframe_and_protected_attribute(
            self.dataset)

        # df should be the same and protected attributz should be None
        assert df.equals(self.dataset)
        assert protected_attribute is None

        # test if one protected attribute
        self.setUp(multi=False)
        baseMitigator = BaseMitigationStrategy()
        df, protected_attribute = baseMitigator._get_dataframe_and_protected_attribute(
            self.dataset, self.protected_attributes)

        # assert that the protected attribute was correctly extracted
        assert protected_attribute == self.protected_attributes[0]
        # assert the df is the same
        assert df.equals(self.dataset)

        # test if multiple protected attributes
        self.setUp(multi=True)
        baseMitigator = BaseMitigationStrategy()
        df, protected_attribute = baseMitigator._get_dataframe_and_protected_attribute(
            self.dataset, self.protected_attributes)

        # assert that the protected attribute was correctly extracted
        assert protected_attribute == "protected_attribute_protected_attribute_2"
        # assert the df has the same columns as the dataset + the new protected one
        assert set(self.dataset.columns.to_list(
        ) + ["protected_attribute_protected_attribute_2"]) == set(df.columns.to_list())
        # assert that the df without the new column is the same as before
        assert self.dataset.equals(
            df.drop(columns=["protected_attribute_protected_attribute_2"]))

    def test_get_final_dataframe(self):
        # test if no protected attribute
        self.setUp()
        baseMitigator = BaseMitigationStrategy()
        df, protected_attribute = baseMitigator._get_dataframe_and_protected_attribute(
            self.dataset)

        final_df = baseMitigator._get_final_dataframe(
            df, None, protected_attribute)
        # final df should be the same as initial dataset
        assert self.dataset.equals(final_df)

        # test if one protected attribute
        self.setUp()
        baseMitigator = BaseMitigationStrategy()
        df, protected_attribute = baseMitigator._get_dataframe_and_protected_attribute(
            self.dataset, self.protected_attributes)

        final_df = baseMitigator._get_final_dataframe(
            df, self.protected_attributes, protected_attribute)

        # final df should be the same as initial dataset
        assert self.dataset.equals(final_df)

        # test if multiple protected attribute
        self.setUp(multi=True)
        baseMitigator = BaseMitigationStrategy()
        df, protected_attribute = baseMitigator._get_dataframe_and_protected_attribute(
            self.dataset, self.protected_attributes)

        final_df = baseMitigator._get_final_dataframe(
            df, self.protected_attributes, protected_attribute)

        # final df should be the same as initial dataset
        assert self.dataset.equals(final_df)
