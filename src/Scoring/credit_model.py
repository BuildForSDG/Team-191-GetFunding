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
def create_credit_limit_model(x_train, y_train):
    """
    Create the model.
    Declare a LogisticRegression object, and make predictions add
    things used to make the model and fit it to the data frame.
    Return a model thst is used to predict default.
    """
    linear_reg = LinearRegression(normalize=True, n_jobs=2)
    ## fit the model with data
    saved_linear_reg = linear_reg.fit(x_train, y_train)
    return saved_linear_reg

# Create the model using the function above.
credit_limit_model = create_credit_limit_model(x_train, y_train)


# Create a file called model_prediction, and open the file.
filename = 'credit_prediction'
outfile = open(filename, 'wb')


# Save the model by dunping it into the file
pickle.dump(credit_limit_model,outfile)
outfile.close()