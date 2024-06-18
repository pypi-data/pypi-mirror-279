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
                            ) :
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

    if protected_attributes is None :
        return train_test_split(dataset, target,
                                test_size=test_size,
                                train_size=train_size,
                                random_state=random_state,
                                shuffle=shuffle,
                                stratify=None)

    else :

        # Bad practice but convenient
        temp_mitigator = BaseMitigationStrategy(None)
        data, protected_attribute = temp_mitigator._get_dataframe_and_protected_attribute(dataset, protected_attributes)

        X_train, X_test, y_train, y_test = train_test_split(data, target,
                                                            test_size=test_size,
                                                            train_size=train_size,
                                                            random_state=random_state,
                                                            shuffle=shuffle,
                                                            stratify=data[protected_attribute])

        if len(protected_attributes) > 1 :
            X_train = X_train.drop(columns=[protected_attribute])
            X_test = X_test.drop(columns=[protected_attribute])


        if mitigator is None :
            # Do not transform the trainign set, just return to train test split
            return X_train, X_test, y_train, y_test

        else :
            # balance the training data before returning the split
            balanced_X_train, balanced_y_train = mitigator.resample(dataset, target, protected_attributes, cont_columns, cat_columns)
            return balanced_X_train, X_test, balanced_y_train, y_test
