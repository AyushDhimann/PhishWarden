import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('online-valid.csv')

# Drop the columns you want to delete
df = df.drop(['phish_id','phish_detail_url','submission_time','verified','verification_time','online','target'], axis=1)

# Write the updated DataFrame to a new CSV file
df.to_csv('online-valid-scrapped.csv', index=False)