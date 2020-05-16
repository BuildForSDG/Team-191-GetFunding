"""
Create a synthetic dataframe.
This module is used to generate datasets that are used for model development.
"""

import random
import pandas as pd
import numpy as np
import os
from datetime import date
from functools import reduce


start_date = date(2020, 1, 1)
end_date = date(2020, 4, 1)
# check is used in the create_dataset function to generate date column
random_dates = pd.date_range(start_date, end_date).to_list()


def create_dataset(num=1):
    """
    Generate a synthetic dataset.
    Given an integer of the number of rows expected in the data set
    Generate a trasaction date column, transaction details column, and
    the transaction status columns for the transaction dataset.
    """
    output = [
              {"trans_date": np.random.choice(random_dates),
               "trans_details": np.random.choice(["airtime_purchase",
                                                  "customer_transfer",
                                                  "deposit_funds",
                                                  "withdrawal",
                                                  "funds_received"],
                                                 p=[0.2, 0.2, 0.2, 0.2, 0.2]),
               "trans_status": np.random.choice(["completed", "reversed",
                                                 "procesing"],
                                                p=[0.9, 0.05, 0.05])
               }
              for x in range(num)
            ]
    return output


trans_dataset = pd.DataFrame(create_dataset(num=60000))


def create_trans_ids(df):
    """
    Add transaction_id and borrower_id.
    Given a data frame generate transaction id which is unique for
    every row and a borrower id which is not unique to every row.
    Add the ids to the data frame and return the data frame.
    """
    df["transaction_id"] = list(range(1, 60001))
    df["borrower_id"] = np.random.choice(list(range(1, 5000)),
                                         size=60000, replace=True)
    return df


trans_dataset = create_trans_ids(trans_dataset)


def create_sub_dataset(df, containing, column_filter, myrange):
    """
    Separate transactional data set into subsets.
    Given a dataframe, filter the dataframe for rows containing
    'containing', on column 'column_filter' and generate a list of
    random numbers as the amount and add the amount as a column
    to the data frame. Add a column of charge as 3 percent of the
    amount and return a dataframe.
    """
    df = df[df[str(column_filter)].str.contains(str(containing))]
    df["amount"] = np.random.choice(list(myrange),
                                    size=len(df["trans_status"]),
                                    replace=True)
    if not containing == "airtime":
        df["charge"] = df["amount"] * 0.03
    else:
        df["charge"] = df["amount"] * 0
    return df

def combine_trans_sets():
    withdrawals = create_sub_dataset(trans_dataset, "withdrawal",
                                     "trans_details", range(100, 30000))
    customer_transfers = create_sub_dataset(trans_dataset, "transfer",
                                            "trans_details", range(100, 35000))
    deposits = create_sub_dataset(trans_dataset, "deposit",
                                  "trans_details", range(100, 70000))
    airtime_purchases = create_sub_dataset(trans_dataset, "airtime",
                                           "trans_details", range(100, 5000))
    funds_received = create_sub_dataset(trans_dataset, "funds_received",
                                        "trans_details", range(100, 35000))
    combined_df =  withdrawals.append([customer_transfers, funds_received,
                                       deposits, airtime_purchases])
    return combined_df.sort_values(by=['transaction_id'])


trans_dataset = combine_trans_sets()


def create_loan_dataset(num=1):
    """ Generate a loan data set.
    Generate a repayment period a date disbursed and a loan amount.
    """
    output = [
              {"repayment_period": np.random.choice([1, 2, 3],
                                                    p=[0.7, 0.2, 0.1]),
               "date_disbursed": np.random.choice(random_dates),
               "loan_amount": random.randrange(100, 35000, 5)
               }
              for x in range(num)
             ]
    return output


loan_dataset = pd.DataFrame(create_loan_dataset(num=20000))


def add_loan_columns(df, num):
    """
    Add date_repaid, loan_id, and borrower_id to loan data.
    Generate additional columns for the loan dataset.
    Given a dataframe generate a date repaid column as the
    date_disbursed plus the repayment_period. Add a loan_id
    of unique loans and a borrower id which is not unique.
    """
    df["date_repaid"] = np.where(df.repayment_period == 1,
                                 df["date_disbursed"] +
                                 pd.offsets.MonthOffset(1),
                                 np.where(df.repayment_period == 2,
                                          df["date_disbursed"] +
                                          pd.offsets.MonthOffset(2),
                                          df["date_disbursed"] +
                                          pd.offsets.MonthOffset(3)))
    df["loan_id"] = list(range(1, len(df["date_repaid"]) + 1))
    df["borrower_id"] = np.random.choice(list(range(1, 5000)),
                                         size=num, replace=True)
    return df


def find_defaulters(df, filters):
    """

    """
    df = df.loc[df["trans_details"].str.contains(str(filters))]
    df = df.groupby(["borrower_id"], as_index=False).agg({'Total_amount':
                                                          'sum'})
    df = df.rename(columns = {"Total_amount": "Total_" + str(filters)})
    return df.sort_values(by=['borrower_id'])
