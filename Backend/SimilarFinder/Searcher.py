import Levenshtein
import heapq
target = input("Enter target string: ")
first_char = target[0].lower()
filename = f"{first_char}.txt"

with open(filename) as f:
    strings = {line.rstrip() for line in f}

# Calculate Levenshtein distance for all strings and get top 3
top_3_strings = heapq.nsmallest(3, strings, key=lambda x: Levenshtein.distance(target, x))


for i, s in enumerate(top_3_strings):
    print()

# Save top 3 most similar strings in a variable
result = list(top_3_strings)
print(result)
