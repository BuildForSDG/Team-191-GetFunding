""" Create a synthetic dataframe.

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
# random_dates is used in the create_dataset function to generate date column
random_dates = pd.date_range(start_date, end_date).to_list()
trans_num = 200000
num_of_borrowers = int(trans_num/20)
num_of_loans = int(trans_num/5)


def create_dataset(num=1):
    """
    Generate a synthetic dataset.
    Given an integer of the num of rows expected in the data set
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
    df = pd.DataFrame(output)
    df["transaction_id"] = list(range(1, trans_num + 1))
    df["borrower_id"] = list(range(1, num_of_borrowers + 1))*20
    return df


trans_dataset = create_dataset(num=trans_num)



def create_sub_dataset(df, containing, column_filter, myrange=None):
    """
    Separate transactional data set into subsets.
    Given a dataframe, filter the dataframe for rows containing
    'containing', on column 'column_filter' and generate a list of
    random nums as the amount and add the amount as a column
    to the data frame. Add a column of charge as 3 percent of the
    amount and return a dataframe.
    """
    df = df[df[str(column_filter)].str.contains(str(containing))]
    if myrange is None:
        df = df.drop(["trans_status"], axis=1)
        return df
    df["amount"] = np.random.choice(list(myrange),
                                    size=len(df["trans_status"]),
                                    replace=True)
    if not containing == "airtime":
        df["charge"] = df["amount"] * 0.03
    else:
        df["charge"] = df["amount"] * 0
    df["total_amount"] = df["charge"] + df["amount"]
    return df


def combine_trans_sets(df):
    withdrawals = create_sub_dataset(df, "withdrawal",
                                     "trans_details", range(100, 5000))
    transfers = create_sub_dataset(df, "transfer",
                                   "trans_details", range(100, 5000))
    deposits = create_sub_dataset(df, "deposit",
                                  "trans_details", range(100, 30000))
    airtime = create_sub_dataset(df, "airtime",
                                 "trans_details", range(100, 5000))
    funds = create_sub_dataset(df, "funds_received",
                               "trans_details", range(100, 35000))
    combined_df = withdrawals.append([transfers, funds, deposits, airtime])
    return combined_df.sort_values(by=['borrower_id'])


trans_dataset = combine_trans_sets(trans_dataset)


def create_loan_dataset(num=1):
    """
    Generate a loan data set.
    Generate a repayment period a date disbursed and a loan amount.
    Then add columns of date_repaid, loan, and borrower ids.
    """
    output = [
              {"repayment_period": np.random.choice([1, 2, 3],
                                                    p=[0.7, 0.2, 0.1]),
               "date_disbursed": np.random.choice(random_dates),
               "loan_amount": random.randrange(100, 35000, 5)
               }
              for x in range(num)
             ]
    df = pd.DataFrame(output)
    df["date_repaid"] = np.where(df.repayment_period == 1,
                                 df["date_disbursed"] +
                                 pd.offsets.MonthOffset(1),
                                 np.where(df.repayment_period == 2,
                                          df["date_disbursed"] +
                                          pd.offsets.MonthOffset(2),
                                          df["date_disbursed"] +
                                          pd.offsets.MonthOffset(3)))
    df["loan_id"] = list(range(1, len(df["date_repaid"]) + 1))
    df["borrower_id"] = list(range(1, num_of_borrowers + 1))*4
    return df


loan_dataset = create_loan_dataset(num=num_of_loans)


def subset_datasets(df, filters):
    """
    Find sum by transaction details.
    Filter data set by transaction details, group by borrower_id, find the sum
    by borrower_id, and rename the total_amount to the total plus the
    transcation details.
    """
    df1 = df.loc[df["trans_details"].str.contains(str(filters))]
    df2 = df1.groupby(["borrower_id"], as_index=False).agg({'total_amount':
                                                          'sum'})
    df3 = df2.rename(columns={"total_amount": "total_" + str(filters)})
    return df3.sort_values(by=['borrower_id'])


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


df_merged = sum_total_details(trans_dataset)


def find_defaulters(df):
    """
    Find defaulters.
    Add a column total_out which is the sum of withdrawal, transfer, and
    airtime. Add a column total_in as the sum of recieved funds and deposits.
    Add a colum of differences as the total_in minus the total_out and set
    defaulter(1) as people who have more money goin out than coming in.
    """
    df["total_out"] = (df["total_withdrawal"] + df["total_transfer"] +
                       df["total_airtime"])
    df["total_in"] = (df["total_deposit"] + df["total_received"])
    df["differences"] = df["total_in"] - df["total_out"]
    df["defaulters"] = np.where(df.differences > 0, 0, 1)
    return df.sort_values(by=['borrower_id'])


final_df = find_defaulters(df_merged)


start_birth_date = date(1950, 1, 1)
end_birth_date = date(2003, 4, 1)
random_birth_dates = pd.date_range(start_birth_date, end_birth_date).to_list()


def create_borrower_dataset(df1, num=1):
    """
    Generate a synthetic dataset.
    Given an integer of the number of rows expected in the data set
    Generate a trasaction date column, transaction details column, and
    the transaction status columns for the transaction dataset.
    Drop unwanted column in the final merged and merge the remaining columns
    to borrower data set on the borrower id.
    """
    output = [
              {"birth_date": np.random.choice(random_dates),
               "borrower_gender": np.random.choice(["male", "female", "other"],
                                                   p=[0.48, 0.48, 0.04])
               }
              for x in range(num)
            ]
    df =  pd.DataFrame(output)
    df["borrower_id"] = list(range(1, num_of_borrowers + 1))
    to_merge = df1.drop(columns=["total_withdrawal", "total_transfer",
                                 "total_deposit", "total_airtime",
                                 "total_received", "total_out",
                                 "total_in", "differences"])
    df = pd.merge(df, to_merge, on="borrower_id", how="left")
    df = df[df['defaulters'].notna()]
    df["defaulters"] = df["defaulters"].astype(int)
    return df


borrower_dataset = create_borrower_dataset(final_df, num_of_borrowers)
# shuffle data set
borrower_dataset = borrower_dataset.sample(frac=1)
#separate data set into a train set and validation set
validation_set = borrower_dataset.head(int(trans_num/2))
train_set = borrower_dataset.tail(int(trans_num/2))



def save_datasets():
    """
    Save datasets.
    check if a data set does not exist in the current working directory
    and save it else do nothing.
    """
    if not os.path.isfile('datasets/loan_dataset.csv'):
        loan_dataset.to_csv('datasets/loan_dataset.csv', header='column_names',
                            index=False)
    if not os.path.isfile('datasets/trans_dataset.csv'):
        trans_dataset.to_csv('datasets/trans_dataset.csv',
                             header='column_names', index=False)
    if not os.path.isfile('datasets/validation_set.csv'):
        validation_set.to_csv('datasets/validation_set.csv',
                                header='column_names', index=False)
    if not os.path.isfile('datasets/train_set.csv'):
        train_set.to_csv('datasets/train_set.csv',
                                header='column_names', index=False)
    return None


save_datasets()
