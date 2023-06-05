import csv

# Set the maximum number of lines to keep
max_lines = 30

# Open the input and output CSV files
with open('../Dataset_Files/online-valid-scrapped.csv', 'r') as input_file, open('../Dataset_Files/online-valid-scrapped-cut.csv', 'w', newline='') as output_file:
    # Create a CSV reader and writer objects
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Write the header row to the output file
    header = next(reader)
    writer.writerow(header)

    # Write up to max_lines rows to the output file
    for i, row in enumerate(reader):
        if i < max_lines:
            writer.writerow(row)
        else:
            break
