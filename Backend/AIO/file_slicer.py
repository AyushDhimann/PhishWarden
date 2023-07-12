import pandas as pd

# Define the line numbers to start and end the cut
start_line = 40460
end_line = 80923

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('online-valid-scrapped.csv')

# Cut the DataFrame from the start line to the end line
cut_df = df.iloc[start_line:end_line]

# Write the cut DataFrame to a new CSV file
cut_df.to_csv('phish-cut.csv', index=False)
