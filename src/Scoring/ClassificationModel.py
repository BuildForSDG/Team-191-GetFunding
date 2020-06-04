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
    if columns_to_encode:
        df = pd.get_dummies(df, columns=columns_to_encode)
    return df





def create_trans_dataset(df):
    df["trans_date"] = pd.to_datetime(df["trans_date"])
    df = df.drop(["trans_status", "total_amount"], axis=1)
    df = dummy_encode_variable(df, ["trans_details"])
    return df


trans_dataset = create_trans_dataset(trans_df)


def create_loan_dataset(df):
    df["date_disbursed"] = pd.to_datetime(df["date_disbursed"])
    df["date_repaid"] = pd.to_datetime(df["date_repaid"])
    return df


loan_dataset = create_loan_dataset(loan_df)


def create_borrower_dataset(df):
    df["birth_date"] = pd.to_datetime(df["birth_date"])
    df = dummy_encode_variable(df, ["borrower_gender"])
    return df


borrower_dataset = create_borrower_dataset(borrower_df)

def create_target_df(df, unique_id, target):
    myTarget = df[[str(unique_id), str(target)]]
    return myTarget


target_df = create_target_df(borrower_dataset, "borrower_id", "defaulters")


def remove_target_from_df(df, column_to_drop):
    df = df.drop([str(column_to_drop)], axis=1)
    return df


final_borrower_dataset = remove_target_from_df(borrower_dataset, "defaulters")
