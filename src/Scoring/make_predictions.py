import pandas as pd
import pickle
import sklearn.metrics as metrics


from ClassificationModel import (borrower_dataset, loan_dataset,
                                 create_target_df, remove_target_from_df,
                                 x_test, y_test)

infile = open("model_prediction",'rb')
default_model = pickle.load(infile)
infile.close()


y_pred=default_model.predict(x_test)
