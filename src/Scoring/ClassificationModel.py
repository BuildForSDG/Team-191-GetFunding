import pandas as pd
import pickle


import featuretools as ft
import featuretools.variable_types as vtypes


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

trans_df = None
loan_df = None
borrower_df = None


if trans_df == None:
    trans_df = pd.read_csv("datasets/trans_dataset.csv")
if loan_df == None:
    loan_df = pd.read_csv("datasets/loan_dataset.csv")
if borrower_df == None:
    borrower_df = pd.read_csv("datasets/train_set.csv")


def dummy_encode_variable(df, columns_to_encode=[]):
    """
    Create dummy variables.

    Given a list of columns and a dataframe convert
    all the provide columns into dummy variables.
    """
    if columns_to_encode:
        df = pd.get_dummies(df, columns=columns_to_encode)
    return df





def create_trans_dataset(df):
    """
    Prepare transactional data for machine learning.

    Convert the trans_date column to a datetime, and drop the trans_status
    columns and total amount. The trans_status is dropped because it may
    impact the model negatively. The total_amount column is dropped
    because it is a sum of amount and charge
    """
    df["trans_date"] = pd.to_datetime(df["trans_date"])
    df = df.drop(["trans_status", "total_amount"], axis=1)
    df = dummy_encode_variable(df, ["trans_details"])
    return df


trans_dataset = create_trans_dataset(trans_df)


def create_loan_dataset(df):
    """
    Prepare loan data for machine learning.

    convert the date_disbursed column to datetime, and the
    date_repaid column to datetime and return a dataframe.
    """
    df["date_disbursed"] = pd.to_datetime(df["date_disbursed"])
    df["date_repaid"] = pd.to_datetime(df["date_repaid"])
    return df


loan_dataset = create_loan_dataset(loan_df)


def create_borrower_dataset(df):
    """
    Prepare borrower data for machine learning.

    Given the loan_dataframe, convert the birth_date to datetime.
    using the dummy_encode_variable function definened above, create
    dummy variables for the borrower_gender column and return the
    final dataframe.
    """
    df["birth_date"] = pd.to_datetime(df["birth_date"])
    df = dummy_encode_variable(df, ["borrower_gender"])
    return df


borrower_dataset = create_borrower_dataset(borrower_df)

def create_target_df(df, unique_id, target):
    """
    Create a dataframe with a unique_id and the target variable.

    Given a dataframe and a column called unique_id create a
    dataframe containing the unique_id and the target columns
    only.
    """
    myTarget = df[[str(unique_id), str(target)]]
    return myTarget


target_df = create_target_df(borrower_dataset, "borrower_id", "defaulters")


def remove_target_from_df(df, column_to_drop):
    """
    Given a dataframe remove the target variable.

    Given a dataframe and a column(the target variable), drop
    the target variable from the dataframe and return a dataframe.
    """
    df = df.drop([str(column_to_drop)], axis=1)
    return df


final_borrower_dataset = remove_target_from_df(borrower_dataset, "defaulters")



def create_transactions_entity_set():
    """
    Create an empty entity set and add entities.

    Initialize an empty entity set called transactions declare all
    variable types present in the transactional dataframe so that
    feature tools can unserstand the variables,
    and add an entity to the emty initalized entity set.
    """
    es = ft.EntitySet(id="transactions")
    transaction_types = {"transaction_id": vtypes.Index,
                         "trans_date": vtypes.Datetime,
                         "amount": vtypes.Numeric,
                         "charge": vtypes.Numeric,
                         "borrower_id": vtypes.Id,
                         "trans_details_airtime_purchase": vtypes.Boolean,
                         "trans_details_customer_transfer": vtypes.Boolean,
                         "trans_details_deposit_funds": vtypes.Boolean,
                         "trans_details_funds_received": vtypes.Boolean,
                         "trans_details_withdrawal": vtypes.Boolean}
    es = es.entity_from_dataframe(entity_id="transactions_data",
                                  dataframe=trans_dataset,
                                  index="transaction_id",
                                  variable_types=transaction_types)
    return es


es =create_transactions_entity_set()


def create_loan_entity_set(es):
    """
    Add the loan dataset to the entity set.

    Given an entity set create variable type from the loan data set,
    create an entity called loan data, and add add the created entityset
    to es and return es(an entyrty set)
    """
    loan_types = {"loan_id": vtypes.Index,
                  "borrower_id": vtypes.Id,
                  "loan_amount": vtypes.Numeric,
                  "date_disbursed": vtypes.Datetime,
                  "date_repaid": vtypes.Datetime,
                  "repayment_period": vtypes.Categorical}
    es = es.entity_from_dataframe(entity_id="loan_data",
                              dataframe=loan_dataset,
                              index="loan_id",
                              variable_types=loan_types)
    return es


es = create_loan_entity_set(es)


def create_borrower_entity_set(es):
    """
    Add borrower entity set to es.

    Given an entityset(es) declare variables types from the borrwer dataset,
    create an entity set call borrwer_data, and add the borrower data
    entity set to the provide enityt set and return the final entiyty set.

    """
    borrower_types = {"borrower_id": vtypes.Index,
                      "birth_date": vtypes.Datetime,
                      "borrower_gender_female": vtypes.Boolean,
                      "borrower_gender_male": vtypes.Boolean,
                      "borrower_gender_other": vtypes.Boolean}
    es = es.entity_from_dataframe(entity_id="borrower_data",
                                  dataframe=final_borrower_dataset,
                                  index="borrower_id",
                                  variable_types=borrower_types)
    return es


es = create_borrower_entity_set(es)


def add_relations_to_es(es):
    """
    Add table relationships to the entity set.

    Given an entity set add relationships between the borrower data
    and the transactions data to the entityset. Also, add the
    relationship between borrower data and loan data to the
    entity set and return the entity set.
    """
    # Relationship between borrower_data and transactions_data
    r_trans_borrowers = ft.Relationship(es["borrower_data"]["borrower_id"],
                                        es["transactions_data"]["borrower_id"])

    # Relationship between borrower_data and loan_data
    r_borrowers_loans = ft.Relationship(es["borrower_data"]["borrower_id"],
                                        es["loan_data"]["borrower_id"])
    es = es.add_relationships([r_trans_borrowers,r_borrowers_loans])
    return es


entity_set = add_relations_to_es(es)
agg_primitives = (["sum", "std", "max", "min", "mean", "count",
                   "mode", "Trend"])


def do_feature_engineering(entity_set, target_entity):
    """
    Create additional features using feature tools.
    Given an entity set and a target entitty, use feature tools
    to create additional features return the index back
    and create a datfame fron the featur matrix created using
    faeture tools.
    """
    feature_matrix, feature_names = ft.dfs(entityset=entity_set,
                                           target_entity=target_entity,
                                           agg_primitives=agg_primitives,
                                           n_jobs=1, verbose=1,
                                           features_only=False)
    feature_matrix.reset_index(inplace = True)
    finaldf = pd.DataFrame(feature_matrix)
    return finaldf


def add_target_to_features(df1, df2, columns_to_drop=[], merge_on=None):
    """
    Return target variable to final_df.
    Remember we removed the taget variable prior to feature engineering.
    Now, given df1 which is the dataframe produced after feature enginnering,
    return the target variable to the data by merging finaldf with target df
    on merge_on and drop the id columns column because they do impact
    prediction and return the resulting dataframe.
    """
    # print("***************************************************")
    # print("***************************************************")
    # print("***************************************************")
    # print(merge_on in df2.columns.to_list())
    final_data = pd.merge(df1, df2, on=merge_on, how="left")
    final_data = final_data.drop(columns_to_drop, axis = 1)
    return final_data