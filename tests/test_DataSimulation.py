"""
Test that data simulation is working.

"""

import unittest
import sys
import warnings


from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_float_dtype
from pandas.api.types import is_datetime64_any_dtype
from pandas.api.types import is_object_dtype


sys.path.append('..')
from src.Scoring.DataSimulation import (
	create_dataset, create_sub_dataset, combine_trans_sets,
	create_loan_dataset, subset_datasets, sum_total_details,
	find_defaulters, create_borrower_dataset, save_datasets,
	pd, trans_num, num_of_borrowers, num_of_loans
	)



create_dataset_columns = (["trans_date", "trans_details", "trans_status",
						   "transaction_id", "borrower_id"])
withdrawal_columns = (["trans_date", "trans_details", "trans_status",
					   "transaction_id", "borrower_id", "amount",
					   "charge", "total_amount"])
combined_columns = ({"airtime_purchase", "deposit_funds", "funds_received",
                     "withdrawal", "customer_transfer"})
create_loan_columns = (["repayment_period", "date_disbursed", "loan_amount",
                        "date_repaid", "loan_id", "borrower_id"])
subset_datasets_columns = ["borrower_id", "total_transfer"]

default_columns = (["borrower_id", "total_withdrawal", "total_transfer",
 	                "total_deposit", "total_airtime", "total_received",
 	                "total_out", "total_in", "differences", "defaulters"])
summed_details = (["borrower_id", "total_withdrawal", "total_transfer",
				  "total_deposit", "total_airtime", "total_received"])
first_borrower_columns = (["birth_date", "borrower_gender", "borrower_id",
                          "defaulters"])


class TransactionalTestCase(unittest.TestCase):
	warnings.filterwarnings("ignore")

	def setUp(self):
		pass

	def test_create_dataset_columns(self):
		df = create_dataset(trans_num)
		df_columns = df.columns.to_list().sort()
		self.assertEqual(df_columns, create_dataset_columns.sort(),
						 msg = """the columns must be  equal to
						 ["trans_date", "trans_details", "trans_status"]""")

	def test_create_dataset_is_dataframe(self):
		df = create_dataset(trans_num)
		self.assertIsInstance(df, pd.DataFrame,
							  msg="The output must be a dataframe.")

	def test_create_dataset_length(self):
		df = create_dataset(trans_num)
		self.assertEqual(len(df.trans_date), trans_num,
						 msg="The length must be equal to trans_num")

	def test_create_dataset_types(self):
		df = create_dataset(trans_num)
		self.assertTrue(is_datetime64_any_dtype(df.trans_date),
						msg="The trans_date column must be of type datetime")
		self.assertTrue(is_object_dtype(df.trans_details),
						msg="The trans_details column must be an object")
		self.assertTrue(is_object_dtype(df.trans_status),
						msg="The is_string_dtype column must be an object")
		self.assertTrue(is_numeric_dtype(df.transaction_id),
						msg="The trans_details column must be an object")
		self.assertTrue(is_numeric_dtype(df.borrower_id),
						msg="The is_string_dtype column must be an object")

	def test_create_sub_dataset(self):
		df = create_dataset(trans_num)
		df1 = create_sub_dataset(df, "withdrawal",
								 "trans_details", range(100, 500))
		df1_columns = df1.columns.to_list().sort()
		confrimed = set(df1.trans_details.to_list())
		self.assertEqual(df1_columns, withdrawal_columns.sort(),
						 msg = """the columns must be  equal to
						 ["trans_date", "trans_details", "trans_status"]""")
		self.assertEqual(confrimed, {"withdrawal"},
						 msg="trans_details should have withdrawal only")

	def test_create_sub_dataset_is_dataframe(self):
		df = create_dataset(trans_num)
		df1 = create_sub_dataset(df, "withdrawal",
								 "trans_details", range(100, 500))
		self.assertIsInstance(df1, pd.DataFrame,
							  msg="The output must be a dataframe.")

	def test_create_sub_dataset_types(self):
		df = create_dataset(trans_num)
		df1 = create_sub_dataset(df, "withdrawal",
								 "trans_details", range(100, 500))
		self.assertTrue(is_datetime64_any_dtype(df.trans_date),
						msg="The trans_date column must be of type datetime")
		self.assertTrue(is_object_dtype(df.trans_details),
						msg="The trans_details column must be an object")
		self.assertTrue(is_object_dtype(df.trans_status),
						msg="The is_string_dtype column must be an object")
		self.assertTrue(is_numeric_dtype(df.transaction_id),
						msg="The trans_details column must be an object")
		self.assertTrue(is_numeric_dtype(df.borrower_id),
						msg="The is_string_dtype column must be an object")

	def test_combine_trans_sets_columns(self):
		df = create_dataset(trans_num)
		df1 = combine_trans_sets(df)
		confrimed = set(df1.trans_details.to_list())
		self.assertEqual(confrimed, combined_columns,
						 msg=("trans_details should have", combined_columns))

	def test_combine_trans_sets_is_dataframe(self):
		df = create_dataset(trans_num)
		df1 = combine_trans_sets(df)
		self.assertIsInstance(df1, pd.DataFrame,
							  msg="combine_trans_sets must be a dataframe.")

	def test_combine_trans_sets_types(self):
		df = create_dataset(trans_num)
		df1 = create_sub_dataset(df, "withdrawal",
								 "trans_details", range(100, 500))
		self.assertTrue(is_datetime64_any_dtype(df.trans_date),
						msg="The trans_date column must be of type datetime")
		self.assertTrue(is_object_dtype(df.trans_details),
						msg="The trans_details column must be an object")
		self.assertTrue(is_object_dtype(df.trans_status),
						msg="The is_string_dtype column must be an object")
		self.assertTrue(is_numeric_dtype(df.transaction_id),
						msg="The trans_details column must be an object")
		self.assertTrue(is_numeric_dtype(df.borrower_id),
						msg="The is_string_dtype column must be an object")

	def test_create_loan_dataset(self):
		df = create_loan_dataset(num_of_loans)
		df_columns = df.columns.to_list().sort()
		self.assertEqual(df_columns, create_loan_columns.sort(),
						 msg = ("Columns should be", create_loan_columns))

	def test_create_loan_datasets_is_dataframe(self):
		df = create_loan_dataset(num_of_loans)
		self.assertIsInstance(df, pd.DataFrame,
							  msg="combine_trans_sets must be a dataframe.")

	def test_create_loan_datasets_length(self):
		df = create_loan_dataset(num_of_loans)
		df_columns = df.columns.to_list().sort()
		self.assertEqual(len(df["date_disbursed"]), num_of_borrowers,
			             msg = ("Length must equal to ", num_of_borrowers))

	def test_create_loan_datasets_types(self):
		df = create_loan_dataset(num_of_loans)
		self.assertTrue(is_datetime64_any_dtype(df.date_disbursed),
						msg="date_disbursed column must be of type datetime")
		self.assertTrue(is_numeric_dtype(df.repayment_period ),
						msg="The trans_details column must be numeric")
		self.assertTrue(is_datetime64_any_dtype(df.date_repaid),
						msg="The date_repaid column must be a date")
		self.assertTrue(is_numeric_dtype(df.loan_amount),
						msg="The borrower_id column must be numeric")
		self.assertTrue(is_numeric_dtype(df.loan_id),
						msg="The trans_details column must be numeric")
		self.assertTrue(is_numeric_dtype(df.borrower_id),
						msg="The borrower_id column must be numeric")

	def test_subset_datasets(self):
		df = create_dataset(trans_num)
		df1 = combine_trans_sets(df)
		df2 = subset_datasets(df1, "transfer")
		confrimed = sorted(set(df2.columns.to_list()))
		self.assertFalse(df2.isnull().values.any(),
			             msg = "The dataframe should not have missing values")
		self.assertEqual(confrimed, sorted(subset_datasets_columns),
						 msg = ("Columns should be", subset_datasets_columns))

	def test_subset_datasets_is_dataframe(self):
		df = create_dataset(trans_num)
		df1 = combine_trans_sets(df)
		df2 = subset_datasets(df1, "transfer")
		self.assertIsInstance(df2, pd.DataFrame,
							  msg="subset_datasets must produce a dataframe.")

	def test_subset_datasets_types(self):
		df = create_dataset(trans_num)
		df1 = combine_trans_sets(df)
		df2 = subset_datasets(df1, "transfer")
		self.assertTrue(is_numeric_dtype(df2.borrower_id ),
						msg="The trans_details column must be numeric")
		self.assertTrue(is_float_dtype(df2.total_transfer),
						msg="The total_transfer column must be of type float")


	def test_sum_total_details(self):
		df = create_dataset(trans_num)
		df1 = combine_trans_sets(df)
		df2 = sum_total_details(df1)
		df3_columns = sorted(df2.columns.to_list())
		self.assertEqual(df3_columns, sorted(summed_details),
						 msg = ("Columns should be", summed_details))

	def test_sum_total_details_is_dataframe(self):
		df = create_dataset(trans_num)
		df1 = combine_trans_sets(df)
		df2 = sum_total_details(df1)
		self.assertIsInstance(df2, pd.DataFrame,
							  msg="subset_datasets must produce a dataframe.")


	def test_find_defaulters(self):
		df = create_dataset(trans_num)
		df1 = combine_trans_sets(df)
		df2 = sum_total_details(df1)
		df3 = find_defaulters(df2)
		self.assertTrue("defaulters" in df3.columns.to_list(),
						msg="A column called defaulters must be present")
		self.assertTrue(is_numeric_dtype(df3.defaulters),
		                msg = "the defaulters column must be numeric")

	def test_find_defaulters_is_dataframe(self):
		df = create_dataset(trans_num)
		df1 = combine_trans_sets(df)
		df2 = sum_total_details(df1)
		df3 = find_defaulters(df2)
		df3_columns = sorted(set(df3.columns.to_list()))
		self.assertIsInstance(df3, pd.DataFrame,
							  msg="subset_datasets must produce a dataframe.")
		self.assertEqual(df3_columns, sorted(default_columns),
						 msg = ("the columns must be  equal to ",
						        sorted(default_columns)))

	def test_find_defaulters_types(self):
		df = create_dataset(trans_num)
		df1 = combine_trans_sets(df)
		df2 = sum_total_details(df1)
		df3 = find_defaulters(df2)
		self.assertTrue(is_numeric_dtype(df3.borrower_id),
						msg="The borrower_id column must be numeric")
		self.assertTrue(is_float_dtype(df3.total_withdrawal),
						msg="The total_withdrawal column must be float")
		self.assertTrue(is_float_dtype(df3.total_deposit),
						msg="The total_deposit column must be float")
		self.assertTrue(is_float_dtype(df3.total_airtime),
						msg="The total_airtime column must be float")
		self.assertTrue(is_float_dtype(df3.total_received),
						msg="The total_received column must be float")
		self.assertTrue(is_float_dtype(df3.total_out),
						msg="The total_out column must be float")
		self.assertTrue(is_float_dtype(df3.total_in),
						msg="The total_in column must be float")
		self.assertTrue(is_float_dtype(df3.differences ),
						msg="The differences column must be float")
		self.assertTrue(is_numeric_dtype(df3.defaulters),
						msg="The defaulters column must be float")


	def test_create_borrower_dataset(self):
		trans_dataset = create_dataset(num=trans_num)
		trans_dataset1 = combine_trans_sets(trans_dataset)
		df_merged = sum_total_details(trans_dataset1)
		final_df = find_defaulters(df_merged)
		df = create_borrower_dataset(final_df, num_of_borrowers)
		df_columns = df.columns.to_list().sort()
		self.assertEqual(df_columns, first_borrower_columns.sort(),
						 msg = ("the columns must be  equal to",
						        first_borrower_columns.sort()))


if __name__ == "__main__":
	unittest.main()
