import pandas as pd

# Read the data from the CSV file
df = pd.read_csv('final.csv')
df

# Assuming you have the data in a DataFrame called 'df'
# Filter the data to include only records with "Heavy rain" or "Monsoonal rain" as the main cause
flood_events = df[(df['Main Cause'] == 'Heavy rain') | (df['Main Cause'] == 'Monsoonal rain')]

# Group the filtered data by state
state_groups = flood_events.groupby('loc')

# Calculate the number of flood events for each state
state_flood_counts = state_groups.size()

# Calculate the total number of events for each state
state_total_counts = df.groupby('loc').size()

# Calculate the historical flooding probability for each state
state_flood_probabilities = (state_flood_counts / state_total_counts) * 100

# Calculate the average severity level for each state
state_avg_severity = state_groups['Severity'].mean()

# Calculate the total number of human fatalities for each state
state_total_fatalities = state_groups['Human fatality'].sum()

# Create a DataFrame with historical flooding probabilities, average severity level, and total human fatalities
result_df = pd.DataFrame({
    'Historical Flooding Probability (%)': state_flood_probabilities,
    'Average Severity Level': state_avg_severity,
    'Total Human Fatalities': state_total_fatalities
})

# Fill NaN values with 0
result_df.fillna(0, inplace=True)

# Sort the DataFrame by all three columns
result_df = result_df.sort_values(by=['Total Human Fatalities', 'Historical Flooding Probability (%)', 'Average Severity Level'], ascending=False)

# Add a unique rank column
result_df['Rank'] = result_df.reset_index().index + 1
result_df = result_df.round(2)