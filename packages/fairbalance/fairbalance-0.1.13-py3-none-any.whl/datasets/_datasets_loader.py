from sklearn.metrics import d2_absolute_error_score
from ucimlrepo import fetch_ucirepo
import pandas as pd
from folktables import ACSDataSource, ACSIncome, ACSEmployment, ACSPublicCoverage, ACSMobility, ACSTravelTime

def load_adult() :
    """
    Load the Adult dataset from the uci ML repository. 
    More info: https://archive.ics.uci.edu/dataset/2/adult
    
    Prediction task to determine the income of individuals in a binary manner. 
    The target column is "income", with values 1 and 0 (1: >50k, 0: <=50k).
    The protected attributes are the columns "sex" and "race" with the protected attributes "Male" and "White".
    
    The dataset goes through preprocessing steps and is not exactly the one shared by UCI. These steps include:
        - Including the target column in the dataset.
        - Removing the "fnlwgt" column.
        - Replacing the values in the target column: ">50K" & ">50K." to 1 and "<=50k" & "<=50k." to 0.
        - dropping the rows with non-defined values.
    
    The returned dataset is ready-to-use.
    
    Returns:
        ([pd.DataFrame, str, list, list]): The dataset, the name of the target column, the list of categorical features and the list of continuous features.
    """
    data = fetch_ucirepo(id=2)
    
    adult_data = data.data.features.copy()
    targets = data.data.targets.copy()
    
    adult_data.loc[:, "income"] = targets
    adult_data = adult_data.drop(columns=["fnlwgt"])
    adult_data["income"] = adult_data["income"].replace({"<=50K.": 0, ">50K.": 1, ">50K": 1, "<=50K": 0})
    adult_data = adult_data.dropna()
    
    categorical_features = ["workclass", "marital-status", "occupation", "relationship", "native-country", "education", "sex", "race"]
    continuous_features = [feature for feature in adult_data.columns if feature not in categorical_features and feature != "income"]
    
    return adult_data, "income", categorical_features,continuous_features

def load_bank_marketing() :
    """
    Load the bank marketing dataset from the uci ML repository. 
    More info: https://archive.ics.uci.edu/dataset/222/bank+marketing
    
    Prediction task to determine if an individual subscribed to a bank offer.
    The target column is "subscribed" with values 1 and 0 (1: "yes", 0: "no").
    The protected attributes is the column "age" with the protected attributes "x>25".
    
    The dataset goes through preprocessing steps and is not exactly the one shared by UCI. These steps include:
        - Including the target column in the dataset.
        - Removing the "poutcome" column.
        - Replacing the values in the target column: "yes" to 1 and "no" to 0.
        - Replacing the non-defined values in the "contact" column as "unknown".
        - dropping the rows with non-defined values.
    
    The returned dataset is ready-to-use.
    
    Returns:
        ([pd.DataFrame, str, list, list]): The dataset, the name of the target column, the list of categorical features and the list of continuous features.
    """
    data = fetch_ucirepo(id=222)
    
    bank_data = data.data.features.copy()
    targets = data.data.targets.copy()
    bank_data.loc[:, "subscribed"] = targets
    
    bank_data["age"] = bank_data["age"].apply(lambda x: "x>25" if x > 25 else "x<=25")
    
    bank_data = bank_data.drop(columns=["poutcome"])
    bank_data["contact"] = bank_data["contact"].fillna("unknown")
    bank_data = bank_data.dropna()
    bank_data["subscribed"] = bank_data["subscribed"].replace({"yes": 1, "no": 0})
    
    categorical_features = ["job", "marital", "education", "default", "housing", "loan", "contact", "month", "day_of_week", "age"]
    continuous_features = [feature for feature in bank_data.columns if feature not in categorical_features and feature != "subscribed"]
    
    return bank_data, "subscribed", categorical_features, continuous_features

def load_KDD_census() :
    """
    Load the bank KDD census income dataset from the uci ML repository. 
    More info: https://archive.ics.uci.edu/dataset/117/census+income+kdd
    
    Prediction task to determine the income of individuals in a binary manner. 
    The target column is "income", with values 1 and 0 (1: >50k, 0: <=50k).
    The protected attributes are the columns "sex" and "race" with the protected attributes "Male" and "White".
    
    The dataset goes through preprocessing steps and is not exactly the one shared by UCI. These steps include:
        - Including the target column in the dataset.
        - Dropping the duplicates columns.
        - Replacing the values in the target column: "50000+." to 1 and "-50000" to 0.
        - dropping the rows with non-defined values.
    
    The returned dataset is ready-to-use.
    
    Returns:
        ([pd.DataFrame, str, list, list]): The dataset, the name of the target column, the list of categorical features and the list of continuous features.
    """
    data = fetch_ucirepo(id=117)
     
    kdd_data = data.data.features.copy()
    targets = data.data.targets.copy()
     
    colum_names = ["age","workclass","industry_code","occupation_code","education","enrolled_in_edu_inst_last_wk",
        "marital_status","major_industry_code","major_occupation_code","race","hispanic_origin","sex","member_of_a_labour_union","reason_for_unemployment",
        "employment_status","capital_gains","capital_losses","dividend_from_stocks","tax_filler_status","region_of_previous_residence","state_of_previous_residence",
        "detailed_household_and_family_stat","detailed_household_summary_in_household","instance_weight","migration_code_change_in_msa","migration_code_change_in_reg",
        "migration_code_move_within_reg","live_in_this_house_1_year_ag","migration_prev_res_in_sunbelt","num_persons_worked_for_employer","family_members_under_18","country_of_birth_father",
        "country_of_birth_mother","country_of_birth_self","citizenship","own_business_or_self_employed","fill_inc_questionnaire_for_veteran's_admin","veterans_benefits","weeks_worked_in_year","wage_per_hour","year"]
    
    kdd_data.columns = colum_names
    kdd_data.loc[:, "income"] = targets
    kdd_data = kdd_data.dropna()
    
    kdd_data = kdd_data.drop_duplicates(keep="first", inplace=False)
    
    kdd_data["income"] = (kdd_data["income"] != "-50000").astype(int)
    
    categorical_features = [
        "workclass","industry_code","occupation_code","education","enrolled_in_edu_inst_last_wk",
        "marital_status","major_industry_code","major_occupation_code","hispanic_origin","member_of_a_labour_union","reason_for_unemployment",
        "employment_status","tax_filler_status","region_of_previous_residence","state_of_previous_residence",
        "detailed_household_and_family_stat","detailed_household_summary_in_household","migration_code_change_in_msa","migration_code_change_in_reg",
        "migration_code_move_within_reg","live_in_this_house_1_year_ag","migration_prev_res_in_sunbelt","family_members_under_18","country_of_birth_father",
        "country_of_birth_mother","country_of_birth_self","citizenship","own_business_or_self_employed","fill_inc_questionnaire_for_veteran's_admin","veterans_benefits","year", "race", "sex"
        ]
    continuous_features = [feature for feature in kdd_data.columns if feature not in categorical_features and feature != "income"]
    
    
    
    return kdd_data, "income", categorical_features, continuous_features

def load_ACS(target="income", survey_year="2018",  states=["CA"], horizon="1-Year",survey='person') :
    """
    Loader for access to datasets derived from the US Census, using the Folktables open source python package.
    More information about the Folktables package: https://github.com/socialfoundations/folktables
    
    Args:
        targ (str, optional): The classification task. Available values are "income", "employment", "publiccoverage", 
        "mobility" and "traveltime". Defaults to "income".
        survey_year (str, optional): The year of the survey. Includes years from 2014. Defaults to "2018".
        states (list, optional): The US state(s) to include in the survey. Defaults to ["CA"].
        horizon (str, optional): Horizon of the survey. Available values are "1-Year" and "5-Year". Defaults to "1-Year".
        survey (str, optional): type of survey. Available values are "person" and "household". Defaults to 'person'.

    Prediction task to determine the given "target" in a binary manner. 
    The target column is encoded with values 1 and 0 (1: >50k, 0: <=50k).
    The protected attributes are the columns "SEX" and "RAC1P" with the protected attributes "1" and "1".
    
    The dataset goes through preprocessing steps and is not exactly the one shared by the ACS. These steps include:
        - Including the target column in the dataset.

    The returned dataset is ready-to-use.

    Returns:
        ([pd.DataFrame, str, list, list]): The dataset, the name of the target column, the list of categorical features and the list of continuous features.
    """
    
    sex_map = {1 : "Male", 2 : "Female"}
    rac1p_map = {1 : "White", 2 : "Black", 3 : "Native_American", 4 : "Native_American", 5 : "Native_American", 6 : "Asian", 7 : "Islander", 8 : "Other", 9 : "Mixed" } 
    data_source = ACSDataSource(survey_year=survey_year, horizon=horizon, survey=survey, root_dir="./datasets/acs_data/raw")
    data = data_source.get_data(states=states, download=True)
    
    if target == "income":
        df, target_df, _ = ACSIncome.df_to_pandas(data)
        categorical_features = ["COW", "SCHL", "MAR", "OCCP", "POBP", "RELP", "WKHP"]
    elif target == "employment":
        df, target_df, _ = ACSEmployment.df_to_pandas(data)
        categorical_features = [ "MAR", "RELP", "DIS", "ESP", "CIT", "MIG", "MIL", "ANC", "NATIVITY", "DEAR", "DEYE", "DREM"]
    elif target == "publiccoverage":
        df, target_df, _ = ACSPublicCoverage.df_to_pandas(data)
        categorical_features = ['MAR','DIS','ESP','CIT','MIG','MIL','ANC','NATIVITY','DEAR','DEYE','DREM','PINCP','ESR','ST','FER']
    elif target == "mobility":
        df, target_df, _ = ACSMobility.df_to_pandas(data)
        categorical_features = ['MAR','DIS','ESP','CIT','MIL','ANC','NATIVITY','RELP','DEAR','DEYE','DREM','GCL','COW','ESR','WKHP','JWMNP','PINCP']
    elif target == "traveltime":
        df, target_df, _ = ACSTravelTime.df_to_pandas(data)
        categorical_features = ['MAR','DIS','ESP','MIG','RELP','PUMA','ST','CIT','OCCP','JWTR','POWPUMA','POVPIP']
        
    target_df = target_df.astype(int)
    target_df = target_df[target_df.columns[0]]
    df.loc[:, target] = target_df
    # df.loc[:,"SEX"] = df["SEX"].apply(lambda x : sex_map[x])
    # df.loc[:,"RAC1P"] = df["RAC1P"].apply(lambda x : rac1p_map[x])
    
    categorical_features.append("SEX")
    categorical_features.append("RAC1P")
    
    continuous_features = [feature for feature in df.columns if feature not in categorical_features and feature != target]
    
    return df, target, categorical_features, continuous_features