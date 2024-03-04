import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def remove_outliers(df):
    # Use Quartiles 
    Q1 = df["Total_Cost"].quantile(0.25)
    Q3 = df["Total_Cost"].quantile(0.75)

    #Find IQR
    IQR = Q3 - Q1

    #Find lower and upper bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    #Remove outliers and Return
    return df[(df["Total_Cost"] > lower_bound) & (df["Total_Cost"] < upper_bound)]

# Function to create the required subplots
def create_season_promotion_plots(df):
    fig, axs = plt.subplots(4, 2, figsize=(14, 20))  # Setup subplots
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    promotion_types = ['BOGO (Buy One Get One)', 'Discount on Selected Items', 'No Promo']
    bins = np.arange(0, 200, 10)  # Define bins for histograms

    # Create empty dataframes to store data
    bin_counts = pd.DataFrame(columns=['Spring', 'Summer', 'Fall', 'Winter'])
    medians = pd.DataFrame(columns=promotion_types, index=seasons)

    for i, season in enumerate(seasons):

        # Filter data for the season calling the remove outliers function
        season_data = remove_outliers(df[df['Season'] == season])
        
        # Create histogram for Total_Cost
        axs[i, 0].hist(season_data['Total_Cost'], bins=bins, edgecolor='black')
        axs[i, 0].set_xlabel(f'{season} Total Cost Histogram')
        axs[i, 0].set_ylabel('Number of Transactions')
        # set our y-ticks
        axs[i, 0].set_yticks(np.arange(0, 1400, 200))


        # Count the number in each bin
        bin_count = np.histogram(season_data['Total_Cost'], bins=bins)[0]
        bin_counts[season] = bin_count

        
        # We do not drop outliers for boxplot as per instructions
        # Using list comprehensions against a data frame for bolean indexing to find the box plots
        axs[i, 1].boxplot([season_data[season_data['Promotion'] == promo_type]['Total_Cost'] for promo_type in promotion_types], 
                          labels = ["BOGO", "Disc Select", "No Promo"])
        axs[i, 1].set_xlabel('Total Cost by Promotion Type')

        # Calculate medians for CSV
        for promo in promotion_types:
            # Calculate median for each promotion type, the loc function fills up rows of the empty median dataframe
            medians.loc[season, promo] = round(season_data[season_data['Promotion'] == promo]['Total_Cost'].median(), 3)

    plt.tight_layout()
    plt.show()


    return bin_counts, medians # Return bin counts and medians

# Read in the data
df = pd.read_csv('transaction_s1.csv')

# Call the function to create plots and CSV files
bin_counts , medians = create_season_promotion_plots(df)
bin_counts.to_csv('q4_bins_s1.csv', index=False)
# When saving to CSV, ensure you're not adding any extra characters
medians["Season"] = medians.index
medians.to_csv('q4_medians_s1_test.csv', index=False)