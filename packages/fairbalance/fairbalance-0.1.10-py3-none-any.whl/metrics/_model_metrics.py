import pandas as pd

def _sanity_check(x_true, y_true, y_pred, attribute, privileged_group) :
    # check that x_true is a dataframe
    assert isinstance(x_true, pd.DataFrame), "features should be in a pandas DataFrame format"
    assert isinstance(y_true, pd.Series) or isinstance(y_true, list), "true output should be in a list or pandas Series format"
    
    assert x_true.shape[0] == len(y_true), "features dataframe and output should have the smae number of elements"
    assert len(y_pred) == len(y_true), "predicted output and true output should have the smae number of elements"
    
    assert attribute in list(x_true.columns), f"{attribute} is not a column of the dataframe"
    assert privileged_group in list(x_true[attribute].unique()), f"{privileged_group} is not a class of {attribute}"

def EO(x_true, y_true, y_pred, attribute, privileged_group) :
    """Equal Opportunity \n
    P(Y' = 1 = 1 | S = 1, Y = 1) - P(Y' = 1 | S = 0, Y = 1).

    Args:
        x_true (_type_): _description_
        y_true (_type_): _description_
        y_pred (_type_): _description_
        attribute (_type_): _description_
        privileged_group (_type_): _description_

    Returns:
        _type_: _description_
    """
    _sanity_check(x_true, y_true, y_pred, attribute, privileged_group)
    
    df = x_true.copy()
    df.loc[:, "y_true"] = y_true
    df.loc[:, "y_pred"] = y_pred
    

    #P(Y'=1 | A=1, Y=1)
    A_1_Y_0 = df.loc[(df[attribute].isin([privileged_group])) & (df["y_true"] == 1)]
    P1 = A_1_Y_0.loc[A_1_Y_0["y_pred"] == 1].shape[0] / A_1_Y_0.shape[0]
    #P(Y'=1 | A=0, Y=1)
    A_0_Y_0 = df.loc[(~df[attribute].isin([privileged_group])) & (df["y_true"] == 1)]
    P0 = A_0_Y_0.loc[A_0_Y_0["y_pred"] == 1].shape[0] / A_0_Y_0.shape[0]

    
    return P1 - P0


def EMO(x_true, y_true, y_pred, attribute, privileged_group) :
    """Equal mis-opportunity \n
    P(Y' = 1 = 1 | S = 1, Y = 0) - P(Y' = 1 | S = 0, Y = 0).

    Args:
        x_true (_type_): _description_
        y_true (_type_): _description_
        y_pred (_type_): _description_
        attribute (_type_): _description_
        privileged_group (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    _sanity_check(x_true, y_true, y_pred, attribute, privileged_group)
    
    df = x_true.copy()
    df.loc[:, "y_true"] = y_true
    df.loc[:, "y_pred"] = y_pred
    
    #P(Y'=1 | A=1, Y=0)
    A_1_Y_0 = df.loc[(df[attribute].isin([privileged_group])) & (df["y_true"] == 0)]
    P1 = A_1_Y_0[A_1_Y_0["y_pred"] == 1].shape[0] / A_1_Y_0.shape[0]
    #P(Y'=1 | A=0, Y=0)
    A_0_Y_0 = df.loc[(~df[attribute].isin([privileged_group])) & (df["y_true"] == 0)]
    P0 = A_0_Y_0[A_0_Y_0["y_pred"] == 1].shape[0] / A_0_Y_0.shape[0]
    
    return P1 - P0
