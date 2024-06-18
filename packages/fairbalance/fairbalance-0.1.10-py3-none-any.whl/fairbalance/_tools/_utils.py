import pandas as pd


def binarize_columns(dataset: pd.DataFrame, columns: list, privileged_classes: dict):
    """
    returns the dataframe with the columns of columns binarized as {protected_class} and non_{protected_class}

    Args:
        dataset (pd.DataFrame): dataset to transform
        columns (list): list of columns to transform
        privileged_classes (dict): dictionnary of the privileged classes for each column

    Returns:
        pd.DataFrame : the transformed dataset
    """
    df = dataset.copy()

    for attribute in columns:
        privileged_group = privileged_classes[attribute]
        def form_group(
            x): return f"non_{privileged_group}" if x != privileged_group else privileged_group
        df.loc[:, attribute] = df[attribute].apply(form_group)

    return df


class sanity_checker:

    def _sanity_check(self, dataset, target=None, positive_output_target=None, protected_attributes=None, privileged_groups=None):
        """
        Checks that are common in all classes of the package.
        """
        assert isinstance(
            dataset, pd.DataFrame), "Dataset should be in a pandas DataFrame format."

        assert isinstance(
            target, pd.DataFrame), "target should be in a pandas DataFrame format."
        # if target :
        #     assert target in list(dataset.columns), f""""{target}" is not a column of the dataframe."""

        if positive_output_target:
            assert positive_output_target in target.squeeze().unique(
            ), f""""{positive_output_target}" is not a value of the target"""

        if protected_attributes:
            assert len(
                protected_attributes) > 0, "Needs at least one protected attribute"

            if privileged_groups:
                for protected_attribute in protected_attributes:
                    assert protected_attribute in privileged_groups.keys(
                    ), f"no privileged group defined for attribute {protected_attribute}"
                    assert privileged_groups[protected_attribute] in dataset[protected_attribute].unique(
                    ), f"{privileged_groups[protected_attribute]} is not a class of {protected_attribute}"
