import pandas as pd
import random

# read the merged CSV file
merged_file = pd.read_csv("smolshuffle.csv")

# shuffle the rows randomly
shuffled_file = merged_file.sample(frac=1, random_state=random.seed())

# write the shuffled file to a new CSV file
shuffled_file.to_csv("molshuffle.csv", index=False)
