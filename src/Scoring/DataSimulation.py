"""
Create a synthetic dataframe.
This module is used to generate datasets that are used for model development.
"""

import random
import pandas as pd
import numpy as np
import os
import pickle
import time
import datetime
from datetime import date, timedelta




start_date = date(2020, 1, 1)
end_date = date(2020, 4, 1)
# check is used in the create_dataset function to generate date column
check = pd.date_range(start_date, end_date).to_list()

def create_trans_dataset(num=1):
    """use faker to generate a synthetic dataset. The amount
    is generated using a different function. The different
    function is below this function and is the immediate
    function below this function"""
    output=[
            {"transaction_id": list(range(1, num)),
             "borrower_id": np.random.choice(list(range(1, 5000)),
                                              size=num, replace=True),
             "trans_date": np.random.choice(check),
             "trans_details":np.random.choice(["airtime_purchase",
                                               "customer_transfer",
                                               "deposit_funds",
                                               "withdrawal_amount"],
                                              p=[0.2, 0.2, 0.2, 0.1, 0.1, 0.2]),
             "trans_status": np.random.choice(["completed", "reversed",
                                               "procesing"],
                                               p=[0.9, 0.05, 0.05])
           }
            for x in range(num)
          ]
    return output

trans_dataset = pd.DataFrame(create_dataset(num=20000))


def create_trans_amount(df):
    """Generates the amount colemn in the trans_dataset.
    generate different amounts given the trans_details in the
    trans_dataset. For example if the trans_details is
    airtime_purchase it generates a random number between 5
    and five thousand. It then adds the trans_amount column
    to the trans_dataset."""

    df['amount'] = np.where(df.trans_details == "airtime_purchase",
                            random.randint(5, 5000),
                            np.where(df.trans_details == "customer_transfer",
                            random.randint(100, 35000),
                            np.where(df.trans_details == "deposit_funds",
                            random.randint(100, 35000),
                            np.where(df.trans_details == "withdrawal_amount",
                            random.randint(100, 35000),
                            np.where(df.trans_details == "withdrawal_charge",
                            random.randint(33, 1000), random.randint(33, 1000)
                            )))))
    df["transaction_id"] = list(range(1, 20001))
    df["borrower_id"] = np.random.choice(list(range(1, 5000)),
                                               size=20000, replace=True)
    return df

trans_dataset = create_trans_amount(trans_dataset)



def create_loan_dataset(num=1):
    """ The amount is generated using a different function.
    The different function is below this function and is the immediate
     function below this function"""
    output=[
            {
             "repayment_period": np.random.choice([1, 2, 3],
                                                  p=[0.7, 0.2, 0.1]),
             "date_disbursed":np.random.choice(check),
             "loan_amount":random.randrange(100,35000,5)
           }
            for x in range(num)
          ]
    return output

def add_loan_columns(df, num):
    df["date_repaid"] = np.where(df.repayment_period == 1,
                            df["date_disbursed"]+ pd.offsets.MonthOffset(1),
                            np.where(df.repayment_period == 2,
                            df["date_disbursed"]+ pd.offsets.MonthOffset(2),
                            df["date_disbursed"]+ pd.offsets.MonthOffset(3)))
    df["loan_id"] =  list(range(1, num+1))
    df["borrower_id"] = np.random.choice(list(range(1, 5000)),
                                                  size=num, replace=True)
    return df