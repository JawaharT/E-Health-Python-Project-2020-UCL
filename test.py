from clean_pandas import CleanPandas
import pandas as pd

test_df = pd.DataFrame({"first_name": ["Charles", "Stephen"],
                            "last_name": ["Darwin", "Hawking"],
                            "ssn": ["555-55-5555", "123-45-6789"]})

result_df, encryption_key, dtype_dict = test_df.clean_pandas.encrypt(["first_name", "last_name","ssn"])

result_df.clean_pandas.decrypt(["first_name", "last_name","ssn"], encryption_key, dtype_dict)