import pandas as pd
import pickle


import featuretools as ft
import featuretools.variable_types as vtypes


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


from ClassificationModel import (create_target_df, do_feature_engineering,
								 add_target_to_features)


from RegressionModel import entity_set, myTarget




final_df = do_feature_engineering(entity_set, "goodloans")
# print("borrower_id" in final_df.columns.to_list())


columns_to_drop = ["loan_id", "borrower_id"]
final_data = add_target_to_features(final_df, myTarget, columns_to_drop,
                                    "loan_id")

# split the data set in test dataset and train dataset.
x_train, x_test, y_train, y_test = train_test_split(final_data,
                                                    final_data.loan_amount,
                                                    test_size=0.25,
                                                    random_state=0)
