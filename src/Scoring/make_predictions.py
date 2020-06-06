import pandas as pd
import pickle
import sklearn.metrics as metrics


from ClassificationModel import (borrower_dataset, loan_dataset,
                                 create_target_df, remove_target_from_df,
                                 x_test, y_test)


# Import the model that was dumped into a file called model_prediction
infile = open("model_prediction",'rb')
# load the model from the file
default_model = pickle.load(infile)
# close the file
infile.close()

# make a prediction
y_pred=default_model.predict(x_test)
