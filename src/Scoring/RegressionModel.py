import pandas as pd
import pickle
import sklearn.metrics as metrics


from ClassificationModel import (borrower_dataset, loan_dataset,
                                 create_target_df, remove_target_from_df)


def merge_borrower_loan(df1, df2):
	"""
	Find undefaulted loans.
	Merge loan dataset to borrower dataset and filter for undefaulted
	loans.
	"""
	df = pd.merge(loan_dataset, borrower_dataset, how='left',
	              on=['borrower_id'])
	df = df.loc[df['defaulters'] == 0]
	del df['defaulters']
	return df

good_loans = merge_borrower_loan(loan_dataset, borrower_dataset)
# print(good_loans.columns)


def remove_ids(df):
	df.drop(['loan_id', 'borrower_id'], axis=1, inplace=True)
	return df