import pandas as pd
import pickle
import sklearn.metrics as metrics


import featuretools as ft
import featuretools.variable_types as vtypes


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


from ClassificationModel import (trans_dataset, borrower_dataset, loan_dataset,
                                 create_target_df, remove_target_from_df,
                                 create_transactions_entity_set)


def merge_borrower_loan(df1, df2):
    """
    Find undefaulted loans.
    Merge loan dataset to borrower dataset and filter for undefaulted
    loans.
    """
    df = pd.merge(loan_dataset, borrower_dataset, how="left",
                  on=["borrower_id"])
    df = df.loc[df["defaulters"] == 0]
    del df["defaulters"]
    return df


good_loans_dataset = merge_borrower_loan(loan_dataset, borrower_dataset)
"""create a data frame with the loan_id and loan_amount alone."""
myTarget = create_target_df(good_loans_dataset, "loan_id", "loan_amount")
"""Remove loan_amount i.e the target variable before creating entity sets."""
final_good_loans = remove_target_from_df(good_loans_dataset, "loan_amount")


def create_good_loans_entity_set():
    """
    Create a goodloans entity set.
    Initialize an empty entity set  called goodloans, declare
    variable types present in the good_loans_dataset, and add
    information from the same data set to the goodloans entity set
    and return an entity set.
    """
    es = ft.EntitySet(id="goodloans")
    good_loans_types = {"repayment_period": vtypes.Categorical,
                        "date_disbursed": vtypes.Datetime,
                        "date_repaid": vtypes.Datetime, "loan_id": vtypes.Index,
                        "borrower_id": vtypes.Id, "birth_date": vtypes.Datetime,
                        "borrower_gender_female": vtypes.Boolean,
                        "borrower_gender_male": vtypes.Boolean,
                        "borrower_gender_other": vtypes.Boolean}
    es = es.entity_from_dataframe(entity_id="goodloans",
                                  dataframe=final_good_loans,
                                  index="loan_id",
                                  variable_types=good_loans_types)
    return es


es = create_good_loans_entity_set()



def create_transactions_entity_set(es):
    """
    Create a transactions entity set.
    Given an etnity set declare variable types from the transactions
    dataset create an entity set called transactions_data add it to the
    entity set, and return the final entity set.
    """
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


es =create_transactions_entity_set(es)


def add_relations_to_es(es):
    """Relationship between good_loans and transactions and add it to es."""
    r_trans_goodloans = ft.Relationship(es["goodloans"]["loan_id"],
                                        es["transactions_data"]["borrower_id"])
    es = es.add_relationships([r_trans_goodloans])
    return es


entity_set = add_relations_to_es(es)

