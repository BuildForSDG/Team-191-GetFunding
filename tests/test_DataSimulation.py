"""

Test that data simulation is working.

"""

import unittest
import sys
sys.path.append('..')


from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_datetime64_any_dtype
from pandas.api.types import is_object_dtype

from src.Scoring.DataSimulation import (
	create_dataset, create_trans_ids, create_sub_dataset, combine_trans_sets,
	create_loan_dataset, add_loan_columns, subset_datasets, sum_total_details,
	find_defaulters, create_borrower_dataset, create_borrower_ids,
	add_defaulters, save_datasets, pd, np
	)

create_dataset_columns = ["trans_date", "trans_details", "trans_status"]
class TransactionalTestCase(unittest.TestCase):

	def test_create_dataset_columns(self):
		df = create_dataset(10)
		df_columns = df.columns.to_list().sort()
		self.assertEqual(df_columns, create_dataset_columns.sort(),
			             msg = """the columns must be  equal to
                         ["trans_date", "trans_details", "trans_status"]""")


	def test_create_dataset_is_dataframe(self):
		df = create_dataset(10)
		self.assertIsInstance(df, pd.DataFrame,
		                      msg="The output must be a dataframe.")

	def test_create_dataset_length(self):
		df = create_dataset(10)
		self.assertEqual(len(df.trans_date), 10,
			            msg="The length must be equal to 10")

	def test_create_dataset_types(self):
		df = create_dataset(10)
		self.assertTrue(is_datetime64_any_dtype(df.trans_date),
			            msg="The trans_date column must be of type datetime")
		self.assertTrue(is_object_dtype(df.trans_details),
			            msg="The trans_details column must be an object")
		self.assertTrue(is_object_dtype(df.trans_status),
			            msg="The is_string_dtype column must be an object")

if __name__ == "__main__":
    unittest.main()
