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
             'staking', 'join', 'group', 'telegram', 'whatsapp', 'discord', 'discord nitro', 'antivirus', 'free',
             'true', 'token']

def print_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"Memory usage: {memory_info.rss / (1024*1024):.2f} MB")

def get_ip(url):
    try:
        ip_address = socket.gethostbyname(url)
        return get_ip(url) if ":" in ip_address else ip_address
    except Exception:
        ip_address = ''
    return ip_address

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

def get_blacklisted_words(url):
    try:
        response = requests.get(url)
        webpage_text = response.text.lower()
        blacklisted_words = [word for word in blacklist if re.search(rf'\b{re.escape(word)}\b', webpage_text)]
    except Exception:
        blacklisted_words = []
    return blacklisted_words

def get_nameserver(url):
    try:
        answers = dns.resolver.resolve(url, 'NS')
        nsdata = [rdata.to_text()[:-1] for rdata in answers]
        output_list = [line.strip() for line in nsdata]
    except Exception:
        output_list = []
    return output_list

def process_row(row):
    url = row[0]
    ip = get_ip(url)
    iframes = get_iframes(url)
    age = get_age(url)
    ssl = get_ssl(url)
    blacklisted_words_count = len(get_blacklisted_words(url))
    nameservers = get_nameserver(url)
    #status_code = get_status_code(url)
    length = len(url)
    blacklisted_words_str = ', '.join(get_blacklisted_words(url))
    return np.concatenate((row, [ip], [iframes], [age], [ssl], [', '.join(nameservers)], [blacklisted_words_count], [length], [blacklisted_words_str]))

def analyze_phishing_urls(input_file, output_file):
    # Record the start time
    start_time = time.perf_counter()

    # Read the input CSV file using pandas
    df = pd.read_csv(input_file)

    # Define the column names for the output DataFrame
    column_names = ['url', 'ip_address', 'iframes', 'age', 'ssl', 'nameserver', 'blacklisted_words_count', 'length_of_url', 'blacklisted_words']

    # Process the rows in parallel using a ThreadPoolExecutor
    output_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=120) as executor:
        futures = [executor.submit(process_row, row) for _, row in df.iterrows()]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            result = future.result()
            output_data.append(result)

    # Create a DataFrame using the output data and the column names
    df_output = pd.DataFrame(output_data, columns=column_names)

    # Write the output data to a CSV file using pandas
    df_output.to_csv(output_file, index=False)

    print("After printing output data in a CSV file ")
    print_memory_usage()

    # Record the end time
    end_time = time.perf_counter()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    print(f"Time taken: {elapsed_time:.6f} seconds")

# Call the function to analyze the phishing URLs
analyze_phishing_urls('modified_phish.csv', 'phish.csv')
