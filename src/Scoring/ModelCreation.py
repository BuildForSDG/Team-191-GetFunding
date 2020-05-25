import pandas as pd
import numpy as numpy


from datetime import date


from DataSimulation import (create_sub_dataset,
	                        create_loan_dataset)





trans_dataset = create_dataset(trans_num)
# withdrawals = create_sub_dataset(trans_dataset, "withdrawal",
#                                  "trans_details", range(100, 5000))
# transfers = create_sub_dataset(trans_dataset, "transfer",
#                                "trans_details", range(100, 5000))
# deposits = create_sub_dataset(trans_dataset, "deposit",
#                               "trans_details", range(100, 30000))
# airtime = create_sub_dataset(trans_dataset, "airtime",
#                              "trans_details", range(100, 5000))
# funds = create_sub_dataset(trans_dataset, "funds_received",
#                            "trans_details", range(100, 35000))
print(funds.head(5))