import pandas as pd

def get_cost_quantiles_of_cities(df, cities):
    """
    This function cauclates quartile ranges for cities
    Args: 
        df: the transcation dataframe
        cities: list of cities
    Returns:
        A new pandas dataframe with City, Q1, Median, and Q3
    """
    
    # use the is in function to get specified cities
    df_filtered = df[df["City"].isin(cities)]

    # Use group-by and quantile functions to get IQR statistics & Most importantly use the unstack function within pandas
    # Unstack Documentation: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.unstack.html
    quartiles_df = df_filtered.groupby("City")["Total_Cost"].quantile([0.25, .5, .75]).unstack()

    #Rename Columns
    quartiles_df.columns = ["Q1","Median","Q3"]

    return quartiles_df.reset_index()

def remove_outliers(df, column):
    """
    This function finds values +- 1.5 for the lower and upper bound of the IQR

    Args:
        df: the transaction dataframe
        column: either the Total Cost, Total Items

    Returns: Same data frame values that aren't outliers
    """
    # obtain Q1, and Q3 for specified column
    Q1 = df[column].quantile(.25)
    Q3 = df[column].quantile(.75)

    # Get IQR
    IQR = Q3 - Q1

    # Now calculate the lower and upper bounds that will be used boolean indexing
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # use boolean indexing to save to values that aren't outliers
    non_outlers = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return non_outlers

def get_mean_std_cost_no_outliers(df, payment):
    """
    This function finds mean and stadard devation for a specfiic payment method
    Args:
        df: the transaction dataframe
        column: either the Total Cost, Total Items

    Returns: Same data frame values that aren't outliers
    """

    # Use boolean indexing to slecet all rows for specfied payment method
    df = df[df["Payment_Method"] == payment]

    # Obtain Mean and Stadard Deveation
    return round(df["Total_Cost"].mean(), 4), round(df["Total_Cost"].std(), 4)

# Usage
df = pd.read_csv("transaction_s1.csv")
cost_quant_cities = get_cost_quantiles_of_cities(df, ["New York"])
filtered_df = remove_outliers(df, "Total_Cost")
mean, stadard_dev = get_mean_std_cost_no_outliers(filtered_df, "Credit Card")