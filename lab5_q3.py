import pandas as pd
import numpy as np

def get_expect_bag_num_by_store(df, store):
    # Step 1: Filter the DataFrame for the given store
    store_df = df[df['Store_Type'] == store]
    
    # Step 2: Get total items series
    total_items = store_df["Total_Items"]

    # Step 3: Use lambda and apply to calucuate the number of bags need per customer
    bags = total_items.apply(lambda x : 1 if x <= 5 else np.ceil(x /5))
    # Note use the np .ceil function as it's simpler, but it represent the same equation "else x // 5 + (x % 5 > 0)"
    # That use floor division + the reminder if it's larger than zero

    # Get the mean and round, 
    return bags.mean().round(4)


df = pd.read_csv("transaction_s1.csv")
print(get_expect_bag_num_by_store(df, 'Supermarket'))


    
