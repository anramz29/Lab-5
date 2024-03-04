import pandas as pd

def get_probability_of_discount(df):
    # Use the column index with the sum method to count number of true, then divide it by the length of the dataframe 
    return (df["Discount_Applied"].sum() / len(df)).round(4)

def get_probability_of_payment_in_cities(df, payment, cities):
    #calcuate the probability of a specific payment method being used in a list of cities
    
    # use isin function
    cities_df = (df[df["City"].isin(cities)])

    # filter the dataframe by payment method, and take Payment_Method column count
    payment_method_count = cities_df[cities_df["Payment_Method"] == payment]["Payment_Method"].count()

    # return the count / payments across all cities
    return (payment_method_count/ len(cities_df)).round(4)


def get_probability_of_product_by_customer(df, product, customer):
    #calcuate the probability of a specific product being purchased by a specific customer, for exampe a student buying honey

    # filter the dataframe by product and customer
    customer_type_df = df[df["Customer_Category"] == customer]

    # get count of customer_type occurences of product using the str.contains method in pandas
    num_products_customer = customer_type_df["Product"].str.contains(product).sum()

    return (num_products_customer / len(customer_type_df)).round(4)



#usage 
df = pd.read_csv("transaction_s1.csv")
print(get_probability_of_discount(df))
print(get_probability_of_payment_in_cities(df, "Cash", ["New York", "Boston"]))
print(get_probability_of_product_by_customer(df, "Honey", "Student"))