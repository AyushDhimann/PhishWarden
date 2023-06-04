import os

# Specify input and output directories
input_dir = "C:/Users/ayush/OneDrive/Desktop/SimilarFinder/"
output_dir = "C:/Users/ayush/OneDrive/Desktop/SimilarFinder/"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize variables
current_char = ""
output_file = None

# Open input file for reading
with open(input_dir + "large_file.txt", "r") as input_file:
    for line in input_file:
        # Get first character of string
        first_char = line[0]

        # If first character is different than current character,
        # close previous output file and open a new one for the new character
        if first_char != current_char:
            if output_file:
                output_file.close()
            output_file = open(output_dir + first_char + ".txt", "w")
            current_char = first_char

        # Write string to output file for current character
        output_file.write(line)

    # Close the last output file
    if output_file:
        output_file.close()
