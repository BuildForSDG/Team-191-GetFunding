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
else if loan_df = None:
    loan_df = pd.read_csv("datasets/loan_dataset.csv")
else if == None:
    borrower_df = pd.read_csv("datasets/train_set.csv")
else:
  pass


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


borrower_dataset = remove_target_from_df(borrower_dataset, "defaulters")


def create_transactions_entity_set():
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
    borrower_types = {"borrower_id": vtypes.Index,
                      "birth_date": vtypes.Datetime,
                      "borrower_gender_female": vtypes.Boolean,
                      "borrower_gender_male": vtypes.Boolean,
                      "borrower_gender_other": vtypes.Boolean}
    es = es.entity_from_dataframe(entity_id="borrower_data",
                                  dataframe=borrower_dataset,
                                  index="borrower_id",
                                  variable_types=borrower_types)
    return es


es = create_borrower_entity_set(es)


def add_relations_to_es(es):
    # Relationship between memberdetails and savings
    r_trans_borrowers = ft.Relationship(es["borrower_data"]["borrower_id"],
                                        es["transactions_data"]["borrower_id"])

    # Relationship between memberdetails and mpesa deposits
    r_borrowers_loans = ft.Relationship(es["borrower_data"]["borrower_id"],
                                        es["loan_data"]["borrower_id"])
    es = es.add_relationships([r_trans_borrowers,r_borrowers_loans])
    return es


entity_set = add_relations_to_es(es)
agg_primitives = (["sum", "std", "max", "min", "mean", "count",
                   "mode", "Trend"])


def do_feature_engineering(entity_set):
    feature_matrix, feature_names = ft.dfs(entityset=entity_set,
                                           target_entity="borrower_data",
                                           agg_primitives=agg_primitives,
                                           n_jobs=1, verbose=1,
                                           features_only=False)
    feature_matrix.reset_index(inplace = True)
    finaldf = pd.DataFrame(feature_matrix)
    return finaldf


finaldf = do_feature_engineering(entity_set)


def add_target_to_features():
    final_data = pd.merge(finaldf, target_df , on = "borrower_id")
    final_data = final_data.drop(["borrower_id"], axis = 1)
    return final_data


final_data = add_target_to_features()
x_train, x_test, y_train, y_test = train_test_split(final_data,
                                                    final_data.defaulters,
                                                    test_size=0.25,
                                                    random_state=0)


def create_model():
    logreg = LogisticRegression(C=1.0, class_weight=None, dual=False,
                                fit_intercept=True, intercept_scaling=1,
                                max_iter=110, multi_class='ovr',
                                n_jobs=1, penalty='l1', random_state=None,
                                solver='liblinear', tol=0.0001, verbose=0,
                                warm_start=False)
    ## fit the model with data
    saved_model = logreg.fit(x_train,y_train)
    return saved_model


default_model = create_model()



filename = 'model_prediction'
outfile = open(filename, 'wb')

pickle.dump(default_model,outfile)
outfile.close()
