import pandas as pd

# read the first CSV file
file1 = pd.read_csv("input1.csv")

# read the second CSV file
file2 = pd.read_csv("input2.csv")

# merge the two files based on a common column
merged_file = pd.merge(file1, file2)

# write the merged file to a new CSV file
merged_file.to_csv("merged_input.csv", index=False)
