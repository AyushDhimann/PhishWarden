# pip install bs4 pythondns dnspython Levenshtein requests tqdm python-whois urllib3 psutil pandas pycryptodome flask

import pandas as pd
import concurrent.futures
import time
import psutil
import requests
import socket
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import dns.resolver
from tqdm import tqdm
import ssl
import whois
import urllib3
import tldextract

urllib3.disable_warnings()

blacklist = ['spam', 'scam', 'fraud', 'phishing', 'gift', 'surprise', 'real', 'legit', 'trusted', 'seller', 'buyer',
             'fast', 'secure', 'login', 'verify', 'account', 'update', 'confirm', 'bank', 'paypal', 'ebay', 'amazon',
             'ebay', 'apple', 'microsoft', 'google', 'facebook', 'instagram', 'twitter', 'snapchat', 'linkedin',
             'youtube', 'whatsapp', 'gmail', 'yahoo', 'outlook', 'hotmail', 'aol', 'icloud', 'instant' 'bitcoin',
             'litecoin', 'ethereum', 'dogecoin', 'binance', 'coinbase', 'coinmarketcap', 'cryptocurrency',
             'cryptocurrencies', 'crypto', 'currency', 'blockchain', 'btc', 'eth', 'ltc', 'doge', 'bch', 'xrp', 'xlm',
             'ada', 'usdt', 'usdc', 'dai', 'wbtc', 'uniswap', 'sushiswap', 'pancakeswap', 'defi', 'decentralized',
             'finance', 'defi', 'yield', 'farming', 'staking', 'staking', 'pool', 'pooling', 'staking', 'staking',
             'staking', 'join', 'group', 'telegram', 'whatsapp', 'discord', 'discord nitro', 'antivirus','free','true','token']

blacklisted_words=[]

# Record the start time
start_time = time.perf_counter()

with open('modified_phish.csv', 'r') as urlfile:
    url=urlfile.readline()

print(url)

urlfile.close()

def print_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"Memory usage: {memory_info.rss / (1024*1024):.2f} MB")

print_memory_usage()

def get_ip(url):
    try:
        ip_address = socket.gethostbyname(url)
        return get_ip(url) if ":" in ip_address else ip_address
    except Exception:
        ip_address = ''
    return ip_address

#YOUR
def get_iframes(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        iframes = soup.find_all('iframe')

    except Exception:
        iframes = '0'
    return iframes

def get_age(url):
    try:
        domain = whois.whois(url)
        if isinstance(domain.creation_date, list):
            delta = datetime.now() - domain.creation_date[0]
        else:
            delta = datetime.now() - domain.creation_date
        age = delta.days
    except Exception:
        age = ''
    return age

def get_ssl(url):
    try:
        context = ssl.create_default_context()
        with requests.get(f'https://{url}', verify=False, timeout=5) as response:
            ssl_present = response.ok
    except Exception:
        ssl_present = False
    return ssl_present

#YOUR

import requests
import dns.resolver

def get_blacklisted_words(url):
    try:
        response = requests.get(url)
        webpage_text = response.text.lower()
        blacklisted_words = [word for word in blacklist if f' {word} ' in f' {webpage_text} ']
        print("hello")
    except Exception:
        blacklisted_words = []

    return blacklisted_words

def get_nameserver(url):
    try:
        answers = dns.resolver.resolve(url, 'NS')
        nsdata = []
        for rdata in answers:
            data = rdata.to_text()
            nsdata.append(data[:-1])
        output_list = [line.strip() for line in nsdata]
    except Exception:
        output_list = []
    return output_list

def get_blacklisted_words_count(url):
    blacklisted_words = get_blacklisted_words(url)
    return len(blacklisted_words)

def get_status_code(url):
    try:
        response = requests.get(f'https://{url}', verify=False, timeout=5)
        if response.status_code != 200:
            response = requests.get(f'http://{url}', verify=False, timeout=5)
        status_code = response.status_code
    except Exception:
        status_code = ''
    return status_code

def get_length(url):
    try:
        length_url = len(url)
    except Exception:
        length_url = ''
    return length_url



# define a function to process a row

# define a function to process a row
def process_row(row):
    url = row[0]
    ip = np.array([get_ip(url)])
    iframes = np.array([get_iframes(url)])
    age = np.array([get_age(url)])
    ssl = np.array([get_ssl(url)])
    blacklisted_words_count = np.array([get_blacklisted_words_count(url)])
    nameservers = get_nameserver(url)
    status_code = np.array([get_status_code(url)])
    length = np.array([get_length(url)])
    blacklisted_words_str = ', '.join(get_blacklisted_words(url))
    return np.concatenate((row, ip, iframes, age, ssl, [', '.join(nameservers)], blacklisted_words_count, status_code, length, [blacklisted_words_str]))

# define the column names for the output DataFrame
column_names = ['url', 'ip_address', 'iframes', 'age', 'ssl', 'nameserver', 'blacklisted_words_count', 'status_code', 'length_of_url', 'blacklisted_words']

# read the input CSV file using pandas
df = pd.read_csv('modified_phish.csv')

# convert the DataFrame to a NumPy array
input_data = df.to_numpy()

# process the rows in parallel using a ThreadPoolExecutor
output_data = []
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    futures = []
    for row in input_data:
        future = executor.submit(process_row, row)
        futures.append(future)
    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
        result = future.result()
        output_data.append(result)

# convert the output data to a NumPy array
output_data = np.array(output_data)

# create a DataFrame using the output data and the column names
df_output = pd.DataFrame(output_data, columns=column_names)

# write the output data to a CSV file using pandas
df_output.to_csv('phish.csv', index=False)

print("After printing output data in a CSV file ")
print_memory_usage()

# Record the end time
end_time = time.perf_counter()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print(f"Time taken: {elapsed_time:.6f} seconds")