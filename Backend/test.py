import pandas as pd
import concurrent.futures
import time
from tqdm import tqdm
import psutil

def print_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"Memory usage: {memory_info.rss / (1024*1024):.2f} MB")

print_memory_usage()

# Record the start time
start_time = time.perf_counter()

def get_ip(url):
    # implementation of get_ip function
    pass

def get_iframes(url):
    # implementation of get_iframes function
    pass

def get_age(url):
    # implementation of get_age function
    pass

def get_ssl(url):
    # implementation of get_ssl function
    pass

def get_blacklisted_words(url):
    # implementation of get_blacklisted_words function
    pass

def get_nameserver(url):
    # implementation of get_nameserver function
    pass

def get_blacklisted_words_count(url):
    # implementation of get_blacklisted_words_count function
    pass

def get_status_code(url):
    # implementation of get_status_code function
    pass

def get_length(url):
    try:
        length_url = len(url)
    except Exception:
        length_url = ''
    return length_url

# define a function to process a row
def process_row(row):
    url = row[0]
    ip = get_ip(url)
    iframes = get_iframes(url)
    age = get_age(url)
    ssl = get_ssl(url)
    blacklisted_words = get_blacklisted_words(url)
    nameserver = get_nameserver(url)
    blacklisted_words_count = get_blacklisted_words_count(url)
    status_code = get_status_code(url)
    length = get_length(url)
    return [url, ip, iframes, age, ssl, iframes, blacklisted_words, nameserver, blacklisted_words_count, status_code, length]

# read the input CSV file using pandas
df = pd.read_csv('Dataset_Files/URLs.csv')

# process the rows in parallel using a ThreadPoolExecutor
output_data = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for index, row in tqdm(df.iterrows(), total=len(df)):
        future = executor.submit(process_row, row)
        futures.append(future)
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        output_data.append(result)

# write the output data to a CSV file using pandas
df_output = pd.DataFrame(output_data, columns=['url', 'ip_address', 'iframes', 'age', 'ssl', 'iframes', 'blacklisted_words', 'nameserver', 'blacklisted_words_count', 'status_code', 'length'])
df_output.to_csv('scraped.csv', index=False)

# Record the end time
end_time = time.perf_counter()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print(f"Time taken: {elapsed_time:.6f} seconds")
print_memory_usage()