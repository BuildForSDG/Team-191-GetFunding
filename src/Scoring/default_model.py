import pandas as pd
import pickle


import featuretools as ft
import featuretools.variable_types as vtypes


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


from ClassificationModel import (entity_set, target_df, agg_primitives,
                                 do_feature_engineering, add_target_to_features)


# Create a dataframe with borrower_id and target variables only.
finaldf = do_feature_engineering(entity_set, "borrower_data")


# The function add target to features also drops ids from the dataframe
# in this case the id column that is dropped is borrower_id.
final_data = add_target_to_features(finaldf, target_df, ["borrower_id"],
                                    "borrower_id")
print(final_data.columns)

# split the data set in test dataset and train dataset.
x_train, x_test, y_train, y_test = train_test_split(final_data,
                                                    final_data.defaulters,
                                                    test_size=0.25,
                                                    random_state=0)


def create_default_model(x_train, y_train):
    """
    Create the model.
    Declare a LogisticRegression object, and make predictions add
    things used to make the model and fit it to the data frame.
    Return a model thst is used to predict default.
    """
    logreg = LogisticRegression(C=1.0, class_weight=None, dual=False,
                                fit_intercept=True, intercept_scaling=1,
                                max_iter=110, multi_class='ovr',
                                n_jobs=2, penalty='l1', random_state=None,
                                solver='liblinear', tol=0.0001, verbose=0,
                                warm_start=False)
    ## fit the model with data
    saved_logreg = logreg.fit(x_train, y_train)
    return saved_logreg

# Create the model using the function above.
default_model = create_model(x_train, y_train)


# Create a file called model_prediction, and open the file.
filename = 'default_prediction'
outfile = open(filename, 'wb')


# Save the model by dunping it into the file
pickle.dump(default_model,outfile)
outfile.close()
