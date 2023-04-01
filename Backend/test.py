import pandas as pd
import concurrent.futures
import time

# Record the start time
start_time = time.perf_counter()

def get_length(url):
    try:
        length_url = len(url)
    except Exception:
        length_url = ''
    return length_url

# define a function to process a row
def process_row(row):
    url = row[0]
    return [url]

# read the input CSV file using pandas
df = pd.read_csv('Dataset_Files/URLs.csv')

# process the rows in parallel using a ThreadPoolExecutor
output_data = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for index, row in df.iterrows():
        future = executor.submit(process_row, row)
        futures.append(future)
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        output_data.append(result)

# write the output data to a CSV file using pandas
df_output = pd.DataFrame(output_data, columns=['url', 'length'])
df_output.to_csv('scraped.csv', index=False)

# Record the end time
end_time = time.perf_counter()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print(f"Time taken: {elapsed_time:.6f} seconds")
