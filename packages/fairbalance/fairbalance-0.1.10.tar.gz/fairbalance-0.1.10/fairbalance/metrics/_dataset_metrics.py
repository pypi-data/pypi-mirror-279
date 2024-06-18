import numpy as np
import pandas as pd
import math


def _sanity_check(X, y, protected_attribute, privileged_group, positive_output):
    assert isinstance(
        X, pd.DataFrame), "dataset needs to be in the pandas DataFrame format"

    assert protected_attribute in X.columns.to_list(), \
        f"{protected_attribute} is not a feature of the dataframe"
    if privileged_group:
        assert privileged_group in list(X[protected_attribute].unique()), \
            f"{privileged_group} is not a class of {protected_attribute}"

    if y is not None:
        assert positive_output in list(y.squeeze().unique()), \
            f"{positive_output} is not a class of the target column"


def _make_df(X, y, protected_attribute):
    df = X.copy()
    target = y.columns[0]
    df = pd.concat([df, y], axis=1)
    df = df.dropna(subset=[protected_attribute])
    return df, target


def DIR(X, y, protected_attribute, privileged_group, positive_output):
    """ Disparate Impact Ratio: \n
    P(Y=1|D=unprivileged)/P(Y=1|D=privileged)

    Parameters
    ----------
    X : pd.DataFrame
        The DataFrame used.
    y : pd.DataFrame
        The target dataframe
    protected_attribute : str
        The protected attribute for which to evaluate the Fairness Score.
    privileged_group : Any
        The privileged group for the protected attribute.
    positive_output : Any
        The positive output of the target.

    Returns
    ----------
    [dict, dict]: The Disparate Impact Ratio of each class of the protected attribute and
    the RMSDIR of the protected attribute.
    """
    _sanity_check(X, y, protected_attribute, privileged_group, positive_output)

    df, target = _make_df(X, y, protected_attribute)

    value_count = df.loc[:, [protected_attribute, target]].groupby(
        [protected_attribute, target]).size().unstack(fill_value=0).stack()

    P_privileged = value_count[privileged_group][positive_output] / \
        value_count[privileged_group].sum()

    # if P_privileged == 0:
    #     raise "Privileged Class does not have any positive output"

    DIRs = {}

    classes = df[protected_attribute].unique()
    for c in classes:
        if c != privileged_group:
            P_unprivileged = value_count[c][positive_output] / \
                value_count[c].sum()
            DIRs[c] = P_unprivileged / P_privileged

    for el in DIRs:
        if DIRs[el] > 1:
            DIRs[el] = 1/DIRs[el]

    # Root Mean Squared DI
    RMSDIR = np.sqrt(np.sum(np.array(list(DIRs.values()))**2)/len(DIRs))

    return DIRs, RMSDIR


def SPD(X, y, protected_attribute, privileged_group, positive_output):
    """Statistical Parity Difference : \n
    P(Y=1|D=unprivileged) - P(Y=1|D=privileged)

    Parameters
    ----------
    X : pd.DataFrame
        The DataFrame used.
    y : pd.DataFrame
        The target dataframe
    protected_attribute : str
        The protected attribute for which to evaluate the Fairness Score.
    privileged_group : Any
        The privileged group for the protected attribute.
    positive_output : Any
        The positive output of the target.

    Returns
    ----------
    [dict]: The Statistical Parity Difference of the protected attribute.
    """
    _sanity_check(X, y, protected_attribute, privileged_group, positive_output)

    df, target = _make_df(X, y, protected_attribute)

    classes = df[protected_attribute].unique()

    value_count = df.loc[:, [protected_attribute, target]].groupby(
        [protected_attribute, target]).size().unstack(fill_value=0).stack()

    P_privileged = value_count[privileged_group][positive_output] / \
        value_count[privileged_group].sum()

    SPDs = {}

    for c in classes:
        if c != privileged_group:
            P_unprivileged = value_count[c][positive_output] / \
                value_count[c].sum()
            SPDs[c] = P_unprivileged - P_privileged

    return SPDs


def PMI(X, y, protected_attribute, privileged_group, positive_output):
    '''Normalized Pointwise Mutual Information : \n
    log(P(Attribute, output)/P(Attribute)P(output)) / log(P(Attribute, output))\n
    Normalized Pointwise Mutual Information Ratio : \n
    PMI(unprivleged_attribute)/PMI(privileged attribute)

    Parameters
    ----------
    X : pd.DataFrame
        The DataFrame used.
    y : pd.DataFrame
        The target dataframe
    protected_attribute : str
        The protected attribute for which to evaluate the Fairness Score.
    privileged_group : Any
        The privileged group for the protected attribute.
    positive_output : Any
        The positive output of the target.

    Returns
    ----------
    [dict, dict, dict]: The Pointwise Mutual Information of each class of the protected attribute,
    The Pointwise Mutual Information of each unprivileged class of the protected attribute, and
    the RMSPMI of the protected attribute.
    '''
    _sanity_check(X, y, protected_attribute, privileged_group, positive_output)

    df, target = _make_df(X, y, protected_attribute)

    classes = df[protected_attribute].unique()
    outputs = df[target].unique()

    value_count = df.loc[:, [protected_attribute, target]].groupby(
        [protected_attribute, target]).size().unstack(fill_value=0).stack()

    PMIs = {}
    nb_rows = df.shape[0]
    for c in classes:
        PMIs[c] = {}
        for out in outputs:

            P_attribute = value_count[c].sum() / nb_rows
            P_output = df[target].value_counts()[out] / nb_rows

            P_attribute_inter_output = value_count[c, out] / nb_rows

            if P_attribute_inter_output != 0:
                PMIs[c][out] = math.log(
                    P_attribute_inter_output/(P_attribute*P_output))/math.log(P_attribute_inter_output)
            else:
                # there is no co-occurence so PMI is -1
                PMIs[c][out] = -1

    PMIRs = {}
    for c in classes:
        if c != privileged_group:
            PMIRs[c] = {}
            for out in outputs:
                if PMIs[privileged_group][out] != 0:
                    PMIRs[c][out] = PMIs[c][out]/PMIs[privileged_group][out]
                else:
                    if PMIs[c][out] == 0:
                        PMIRs[c][out] = 1
                    else:
                        PMIRs[c][out] = np.nan
    # Root Mean Squared PMI
    RMSPMI = 0
    for el in PMIs.values():
        RMSPMI += np.sum(np.array(list(el.values()))**2)

    RMSPMI = np.sqrt(RMSPMI/(len(PMIs)*len(df[target].unique())))

    return PMIs, PMIRs, RMSPMI


def balance(X, y, protected_attribute, privileged_group, positive_output):
    '''
    Balance : \n
    Number of element for each class of the attribute.

    Parameters
    ----------
    X : pd.DataFrame
        The DataFrame used.
    y : pd.DataFrame
        The target dataframe
    protected_attribute : str
        The protected attribute for which to evaluate the Fairness Score.
    privileged_group : Any
        The privileged group for the protected attribute.
    positive_output : Any
        The positive output of the target.

    Returns
    ----------
    [pd.DataFrame]: The number of element of each class of the protected attribute.
    '''
    _sanity_check(X, y, protected_attribute, privileged_group, positive_output)

    df, _ = _make_df(X, y, protected_attribute)
    return df[protected_attribute].value_counts()


def balance_index(X, y, protected_attribute, privileged_group, positive_output):
    '''
    Balance Index : \n
    Normalized Root Mean Squared Distribution Deviation. \n
    sqrt(sum((P(D=class) - 1/Nclass)**2)/Nclass) / sqrt(((1 - 1/Nclass)**2 + (Nclass-1)(0 - 2/Nclass)**2)/Nclass)

    Parameters
    ----------
    X : pd.DataFrame
        The DataFrame used.
    y : pd.DataFrame
        The target dataframe
    protected_attribute : str
        The protected attribute for which to evaluate the Fairness Score.
    privileged_group : Any
        The privileged group for the protected attribute.
    positive_output : Any
        The positive output of the target.

    Returns
    ----------
    [float]: The Balance index of the protected attribute.
    '''
    _sanity_check(X, y, protected_attribute, privileged_group, positive_output)

    df, _ = _make_df(X, y, protected_attribute)

    value_count = df[protected_attribute].value_counts()
    nb_elements = value_count.sum()
    nb_class = value_count.shape[0]

    balance_idx = 0
    for value in value_count:
        balance_idx += (value/nb_elements - 1/nb_class)**2
    balance_idx = math.sqrt(balance_idx/nb_class)

    norm_term = math.sqrt(
        ((1-1/nb_class)**2 + (nb_class-1)*(0-1/nb_class)**2)/nb_class)

    return 1 - balance_idx/norm_term


def CBS(X, y, protected_attribute, privileged_group, positive_output):
    '''Composite Balance Score : \n
    Composite score using the Balance Index, the Disparate Impact Ratio and the Pointwise Mutual Information. \n
    1 - RMS([(balance_index - 1), (RMS(DIR(unprivileged classes)) - 1), (RMS(sum(RMS(PMI(all classes)))))])

    Parameters
    ----------
    X : pd.DataFrame
        The DataFrame used.
    y : pd.DataFrame
        The target dataframe
    protected_attribute : str
        The protected attribute for which to evaluate the Fairness Score.
    privileged_group : Any
        The privileged group for the protected attribute.
    positive_output : Any
        The positive output of the target.

    Returns
    ----------
    [float] : The Composite Fairness Score of the protected attribute.
    '''
    balance_idx = balance_index(
        X, y, protected_attribute, privileged_group, positive_output)

    # get the disparate impact
    _, RMSDIR = DIR(X, y, protected_attribute,
                    privileged_group, positive_output)

    # get the PMI
    _, _, RMSPMI = PMI(X, y, protected_attribute,
                       privileged_group, positive_output)

    score = 1 - math.sqrt(((balance_idx - 1)**2 +
                          (RMSDIR - 1)**2 + RMSPMI**2)/3)

    return score
