"""
Create a synthetic dataframe.
This module is used to generate datasets that are used for model development.
"""

import random
import pandas as pd
import numpy as np
import os
import janitor
import warnings


from datetime import date
from functools import reduce


warnings.filterwarnings('ignore')
start_date = date(2020, 1, 1)
end_date = date(2020, 4, 1)
# check is used in the create_dataset function to generate date column
random_dates = pd.date_range(start_date, end_date).to_list()
trans_number = 100000
number_of_borrowers = 20000
number_of_loans = 20000


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


trans_dataset = pd.DataFrame(create_dataset(num=trans_number))


def create_trans_ids(df):
    """
    Add transaction_id and borrower_id.
    Given a data frame generate transaction id which is unique for
    every row and a borrower id which is not unique to every row.
    Add the ids to the data frame and return the data frame.
    """
    df["transaction_id"] = list(range(1, trans_number + 1))
    df["borrower_id"] = np.random.choice(list(range(1, number_of_borrowers )),
                                         size=trans_number, replace=True)
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
    df["total_amount"] = df["charge"] + df["amount"]
    return df



def combine_trans_sets():
    withdrawals = create_sub_dataset(trans_dataset, "withdrawal",
                                     "trans_details", range(100, 5000))
    customer_transfers = create_sub_dataset(trans_dataset, "transfer",
                                            "trans_details", range(100, 5000))
    deposits = create_sub_dataset(trans_dataset, "deposit",
                                  "trans_details", range(100, 30000))
    airtime_purchases = create_sub_dataset(trans_dataset, "airtime",
                                           "trans_details", range(100, 5000))
    funds_received = create_sub_dataset(trans_dataset, "funds_received",
                                        "trans_details", range(100, 35000))
    combined_df =  withdrawals.append([customer_transfers, funds_received,
                                       deposits, airtime_purchases])
    return combined_df.sort_values(by=['borrower_id'])


trans_dataset = combine_trans_sets()


def create_loan_dataset(num=1):
    """ Generate a loan data set.
    Generate a repayment period a date disbursed and a loan amount.
    """
    output = [
              {"repayment_period": np.random.choice([1, 2, 3],
                                                    p=[0.7, 0.2, 0.1]),
               "date_disbursed": np.random.choice(random_dates),
               "loan_amount": random.randrange(100, 35000 , 5)
               }
              for x in range(num)
             ]
    return output


loan_dataset = pd.DataFrame(create_loan_dataset(num=number_of_loans))


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
    df["borrower_id"] = np.random.choice(list(range(1, number_of_borrowers )),
                                         size=num, replace=True)
    return df



def subset_datasets(df, filters):
    """
    Find sum by transaction details.
    Filter data set by transaction details, group by borrower_id, find the sum
    by borrower_id, and rename the total_amount to the total plus the
    transcation details.
    """
    df = df.loc[df["trans_details"].str.contains(str(filters))]
    df = df.groupby(["borrower_id"], as_index=False).agg({'total_amount':
                                                          'sum'})
    df=df.rename(columns = {"total_amount": "total_" + str(filters)})
    return df.sort_values(by=['borrower_id'])



def sum_total_details(df):
    """
    Find the sum of transactional detail by borrower_id.
    Use subset_datasets to find the total of every transaction for every
    borrower_id and merge the resulting data sets (outer join to keep
    rows from all data sets) and fill Nans with zero.
    """
    withdrawal = subset_datasets(df, "withdrawal")
    customer_transfers = subset_datasets(df, "transfer")
    deposits = subset_datasets(df, "deposit")
    airtime_purchases = subset_datasets(df, "airtime")
    funds_received = subset_datasets(df, "received")
    # Merge dataframes by borrower_id and fill missing values with zero
    data_frames = [withdrawal, customer_transfers,
                   deposits, airtime_purchases, funds_received]
    df_merged = reduce(lambda left, right: pd.merge(left, right,
                                                    on=['borrower_id'],
                                                    how='outer'),
                       data_frames)
    df_merged = df_merged.fillna(0)
    return df_merged


def find_defaulters(df):
    """
    Find defaulters.
    Add a column total_out which is the sum of withdrawal, transfer, and airtime.
    Add a column total_in as the sum of recieved funds and deposits.
    Add a colum of differences as the total_in minus the total_out and set
    defaulter(1) as people who have more money goin out than coming in.
    """
    df["total_out"] = (df["total_withdrawal"] + df["total_transfer"]
                       + df["total_airtime"])
    df["total_in"] = (df["total_deposit"] + df["total_received"])
    df["differences"] = df["total_in"] - df["total_out"]
    df["defaulters"] = np.where(df.differences > 0, 0, 1)
    return df.sort_values(by=['borrower_id'])


final_df = find_defaulters(df_merged)


start_birth_date = date(1950, 1, 1)
end_birth_date = date(2003, 4, 1)
random_birth_dates =  pd.date_range(start_birth_date, end_birth_date).to_list()


def create_borrower_dataset(num=1):
    """
    Generate a synthetic dataset.
    Given an integer of the number of rows expected in the data set
    Generate a trasaction date column, transaction details column, and
    the transaction status columns for the transaction dataset.
    """
    output = [
              {"birth_date": np.random.choice(random_dates),
               "borrower_gender": np.random.choice(["male", "female", "other"],
                                                 p=[0.48, 0.48, 0.04])
               }
              for x in range(num)
            ]
    return output


borrower_dataset = pd.DataFrame(create_borrower_dataset(number_of_borrowers))

def create_borrower_ids(df):
    """
    Add borrower_id.
    Given a data frame and a borrower id which is unique to every row.
    Add the ids to the data frame and drop unwanted columns in the
    final_df and merge the two dataframes.
    """
    df["borrower_id"] = list(range(1, number_of_borrowers + 1))
    return df

borrower_dataset = create_borrower_ids(borrower_dataset)


def add_defaulters(df1, df2):
    to_merge = df1.drop(columns=["total_withdrawal", "total_transfer",
                                      "total_deposit", "total_airtime",
                                      "total_received", "total_out",
                                      "total_in", "differences"])
    df = pd.merge(df2, to_merge, on = "borrower_id", how = "left")
    df["defaulters"] = df["defaulters"].astype(int)
    return df


borrower_dataset = add_defaulters(final_df, borrower_dataset)
