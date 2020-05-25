import pandas as pd
import numpy as np


from datetime import date


import featuretools as ft
import featuretools.variable_types as vtypes



def dummy_encode_variable(df, columns_to_encode=[]):
    if columns_to_encode:
        df = pd.get_dummies(df, columns=columns_to_encode)
    return df


def create_trans_dataset():
    df = pd.read_csv("datasets/trans_dataset.csv")
    df["trans_date"] = pd.to_datetime(df["trans_date"])
    df = df.drop(["trans_status", "total_amount"], axis=1)
    df = dummy_encode_variable(df, ["trans_details"])
    return df


trans_dataset = create_trans_dataset()


def create_loan_dataset():
    df = pd.read_csv("datasets/loan_dataset.csv")
    df["date_disbursed"] = pd.to_datetime(df["date_disbursed"])
    df["date_repaid"] = pd.to_datetime(df["date_repaid"])
    return df

loan_dataset = create_loan_dataset()

def create_borrower_dataset():
    df = pd.read_csv("datasets/borrower_dataset.csv")
    df["birth_date"] = pd.to_datetime(df["birth_date"])
    df = dummy_encode_variable(df, ["borrower_gender"])
    return df


borrower_dataset = create_borrower_dataset()

def create_target_df(df, unique_id, target):
    myTarget = df[[str(unique_id), str(target)]]
    return myTarget


target_df = create_target_df(borrower_dataset, "borrower_id", "defaulters")


def remove_target_from_df(df, column_to_drop):
    df = df.drop([str(column_to_drop)], axis=1)
    return df


borrower_dataset = remove_target_from_df(borrower_dataset, "defaulters")