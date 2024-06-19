import pandas as pd
from sklearn.model_selection import train_test_split
from ..mitigation_strategies.base import BaseMitigationStrategy


def balanced_train_test_split(dataset,
                              target,
                              protected_attributes=None,
                              mitigator=None,
                              cont_columns=None,
                              cat_columns=None,
                              *,
                              test_size=None,
                              train_size=None,
                              random_state=None,
                              shuffle=True,
                              ):
    """makes for a better balanced train_test_split. \n
    - If protected_attributes is None, returns a normal train test split using sklearn train_test_split.
    - If protected_attributes is defined but mitigator is None, returns a train_test_split for which the distribution of classes of the protected attributes
    are the same in the training and testing set, and similar to that of the initial dataset.
    - If both protected_attributes and mitigator are defined, balances the training data using the given mitigator before returning the split.

    Parameters
    ----------
    dataset : pd.DataFrame
        The dataset to balance, without the target column.
    target : pd.Series
        The target column.
    protected_attributes : list, optional
        The protected attribute(s) for which to keep the balance. Defaults to None.
    mitigator : BaseMitigationStrategy, optional
        The mitigation strategy object to use to balance the train data. Defaults to None.
    cont_columns : list, optional
        The names of the continuous columns of the dataset. Only necessary if mitigator is defined. Defaults to None.
    cat_columns : list, optional
        The names of the categorical columns of the dataset. Only necessary if mitigator is defined. Defaults to None.

    all the other arguments are the standard argument for sklearn train_test_split.

    Returns
    ----------
    [pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: X_train, X_test, y_train, y_test
    """

    data = dataset.copy()
    if not mitigator:
        if protected_attributes is None:
            # there is no mitigator not protected attribute: normal train test split
            return train_test_split(data, target.squeeze(),
                                    test_size=test_size,
                                    train_size=train_size,
                                    random_state=random_state,
                                    shuffle=shuffle,
                                    stratify=None)

        else:
            # There is no mitigator but protected attribute: stratify over the protected attribute
            # Bad practice but convenient
            temp_mitigator = BaseMitigationStrategy(None)
            data, protected_attribute = temp_mitigator._get_dataframe_and_protected_attribute(
                dataset, protected_attributes)

            X_train, X_test, y_train, y_test = train_test_split(data, target.squeeze(),
                                                                test_size=test_size,
                                                                train_size=train_size,
                                                                random_state=random_state,
                                                                shuffle=shuffle,
                                                                stratify=data[protected_attribute])

            if len(protected_attributes) > 1:
                X_train = X_train.drop(columns=[protected_attribute])
                X_test = X_test.drop(columns=[protected_attribute])

            return X_train, X_test, y_train, y_test

    else:
        if protected_attributes is None:
            X_train, X_test, y_train, y_test = train_test_split(data, target.squeeze(),
                                                                test_size=test_size,
                                                                train_size=train_size,
                                                                random_state=random_state,
                                                                shuffle=shuffle)
        else:
            temp_mitigator = BaseMitigationStrategy(None)
            data, protected_attribute = temp_mitigator._get_dataframe_and_protected_attribute(
                dataset, protected_attributes)
            X_train, X_test, y_train, y_test = train_test_split(data, target.squeeze(),
                                                                test_size=test_size,
                                                                train_size=train_size,
                                                                random_state=random_state,
                                                                shuffle=shuffle,
                                                                stratify=data[protected_attribute])

            if len(protected_attributes) > 1:
                X_train = X_train.drop(columns=[protected_attribute])
                X_test = X_test.drop(columns=[protected_attribute])

        balanced_X_train, balanced_y_train = mitigator.resample(
            X_train, y_train.to_frame(), protected_attributes, cont_columns, cat_columns)
        return balanced_X_train, X_test, balanced_y_train.squeeze(), y_test
