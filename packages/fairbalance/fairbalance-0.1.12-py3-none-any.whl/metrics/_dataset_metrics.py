import numpy as np
import pandas as pd
import math

def _sanity_check(df, attribute, privileged_group, target, positive_output) :
    #check that df is in the dataframe format
    assert isinstance(df, pd.DataFrame), "dataset needs to be in the pandas DataFrame format"    
    
    # sanity check for attribute 
    assert attribute in list(df.columns), f"{attribute} is not a feature of the dataframe"
    if privileged_group :
        assert privileged_group in list(df[attribute].unique()), f"{privileged_group} is not a class of {attribute}"
    
    # sanity check for target
    if target :
        assert target in list(df.columns), f"{target} is not a column of the dataframe"
        assert positive_output in list(df[target].unique()), f"{positive_output} is not a class of {target}"
    
    
def DIR(df, attribute, privileged_group, target, positive_output) :
    """P(Y=1|D=unprivileged)/P(Y=1|D=privileged)

    Args:
        df (pd.DataFrame): _description_
        attribute (str): _description_
        privileged_group (str | int | float): _description_
        target (str): _description_
        positive_output (str | int | float): _description_

    Returns:
        _type_: _description_
    """
    _sanity_check(df, attribute, privileged_group, target, positive_output)
    
    df = df.dropna(subset=[attribute])

    classes = df[attribute].unique()

  
    value_count = df.loc[:, [attribute, target]].groupby([attribute, target]).size().unstack(fill_value=0).stack()
    
    P_privileged = value_count[privileged_group][positive_output] / value_count[privileged_group].sum()
    
    # if P_privileged == 0:
    #     raise "Privileged Class does not have any positive output"
    
    DIRs = {}
    
    for c in classes :
        if c != privileged_group :
            P_unprivileged = value_count[c][positive_output] / value_count[c].sum()
            DIRs[c] = P_unprivileged / P_privileged
                
    for el in DIRs:
        if DIRs[el] > 1 :
            DIRs[el] = 1/DIRs[el]

    #Root Mean Squared DI
    RMSDIR = np.sqrt(np.sum(np.array(list(DIRs.values()))**2)/len(DIRs))
    
    return DIRs, RMSDIR



def SPD(df, attribute, privileged_group, target, positive_output) :
    """Statistical Parity Difference : \n
    P(Y=1|D=unprivileged) - P(Y=1|D=privileged)

    Args:
        df (pd.DataFrame): _description_
        attribute (str): _description_
        privileged_group (str | int | float): _description_
        target (str): _description_
        positive_output (str | int | float): _description_
    Returns:
        _type_: _description_
    """
    
    _sanity_check(df, attribute, privileged_group, target, positive_output)
    
    df = df.dropna(subset=[attribute])
    
    classes = df[attribute].unique()
    
    value_count = df.loc[:, [attribute, target]].groupby([attribute, target]).size().unstack(fill_value=0).stack()

    P_privileged = value_count[privileged_group][positive_output] / value_count[privileged_group].sum()
 
    SPDs = {}
    
    for c in classes :
            if c != privileged_group :
                P_unprivileged = value_count[c][positive_output] / value_count[c].sum()
                SPDs[c] = P_unprivileged - P_privileged
    
    return SPDs


def PMI(df, attribute, privileged_group, target, positive_output = None) :
    '''
    Normalized Pointwise Mutual Information : \n
    log(P(Attribute, output)/P(Attribute)P(output))/log(P(Attribute, output))\n 
    Normalized Pointwise Mutual Information Ratio : \n
    PMI(unprivleged_attribute)/PMI(privileged attribute)
    '''
    
    _sanity_check(df, attribute, privileged_group, target, positive_output)
    
    df = df.dropna(subset=[attribute])
    
    classes = df[attribute].unique()
    outputs = df[target].unique()
    
    value_count = df.loc[:, [attribute, target]].groupby([attribute, target]).size().unstack(fill_value=0).stack()
    
    PMIs = {} 
    nb_rows = df.shape[0]
    for c in classes :
        PMIs[c] = {}             
        for out in outputs :

            P_attribute = value_count[c].sum() / nb_rows
            P_output = df[target].value_counts()[out] / nb_rows
            
                
            P_attribute_inter_output = value_count[c, out] / nb_rows
            
            if P_attribute_inter_output != 0 :
                PMIs[c][out] = math.log(P_attribute_inter_output/(P_attribute*P_output))/math.log(P_attribute_inter_output)
            else :
                #there is no co-occurence so PMI is -1
                PMIs[c][out] = -1
            
                        
    PMIRs = {}
    for c in classes :
        if c != privileged_group :
            PMIRs[c] = {}   
            for out in outputs :
                if PMIs[privileged_group][out] != 0 :
                    PMIRs[c][out] = PMIs[c][out]/PMIs[privileged_group][out]            
                else :
                    if PMIs[c][out] == 0 :
                        PMIRs[c][out] = 1
                    else :
                        PMIRs[c][out] = np.nan
    #Root Mean Squared PMI
    RMSPMI = 0
    for el in PMIs.values() :
        RMSPMI += np.sqrt(np.sum(np.array(list(el.values()))**2))
    RMSPMI = np.sqrt(RMSPMI/(len(PMIs)*len(df[target].unique())))
    
    return PMIs, PMIRs, RMSPMI


def balance(df, attribute, privileged_group = None, target = None, positive_output = None) : 
    '''
    Balance : \n
    Number of element for each class of the attribute.
    '''
    _sanity_check(df, attribute, privileged_group, target, positive_output)
    return df[attribute].value_counts()


def balance_index(df, attribute, privileged_group = None, target = None, positive_output = None) :
    '''
    Balance Index : \n
    Normalized Root Mean Squared Distribution Deviation \n
    sqrt(sum((P(D=class) - 1/Nclass)**2)/Nclass) / sqrt(((1 - 1/Nclass)**2 + (Nclass-1)(0 - 2/Nclass)**2)/Nclass)
    '''
    _sanity_check(df, attribute, privileged_group, target, positive_output)
    
    value_count = df[attribute].value_counts()  
    nb_elements = value_count.sum()
    nb_class = value_count.shape[0] 
    
    balance_idx = 0
    for value in value_count :
        balance_idx += (value/nb_elements - 1/nb_class)**2   
    balance_idx = math.sqrt(balance_idx/nb_class)
    
    norm_term = math.sqrt(((1-1/nb_class)**2 + (nb_class-1)*(0-1/nb_class)**2)/nb_class)
    
    return 1 - balance_idx/norm_term


def FS(df, attribute, privileged_group, target, positive_output) :
    '''
    Fairness score : \n
    Composite score using the Balance Index, the Disparate Impact Ratio and the Pointwise Mutual Information. \n
    1 - RMS([(balance_index - 1), (RMS(DIR(unprivileged classes)) - 1), (RMS(sum(RMS(PMI(all classes)))))])
    '''
    #get the balance index
    balance_idx = balance_index(df,
                                attribute,
                                privileged_group,
                                target,
                                positive_output)
    
    #get the disparate impact
    _, RMSDIR = DIR(df,
                 attribute,
                 privileged_group,
                 target,
                 positive_output)


    #get the PMI
    _, _, RMSPMI = PMI(df,
                     attribute,
                     privileged_group,
                     target,
                     positive_output)
    


    score = 1 - math.sqrt(((balance_idx - 1)**2 + (RMSDIR - 1)**2 + RMSPMI**2)/3)

    return score