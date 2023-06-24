import pandas as pd
import concurrent.futures
import time
import psutil
import requests
import socket
import asyncio
import ssl
import whois
import dns
import urllib3
import re

from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm

urllib3.disable_warnings()

blacklist = ['spam', 'scam', 'fraud', 'phishing', 'gift', 'surprise', 'real', 'legit', 'trusted', 'seller', 'buyer',
             'fast', 'secure', 'login', 'verify', 'account', 'update', 'confirm', 'bank', 'paypal', 'ebay', 'amazon',
             'ebay', 'apple', 'microsoft', 'google', 'facebook', 'instagram', 'twitter', 'snapchat', 'linkedin',
             'youtube', 'whatsapp', 'gmail', 'yahoo', 'outlook', 'hotmail', 'aol', 'icloud', 'instant' 'bitcoin',
             'litecoin', 'ethereum', 'dogecoin', 'binance', 'coinbase', 'coinmarketcap', 'cryptocurrency',
             'cryptocurrencies', 'crypto', 'currency', 'blockchain', 'btc', 'eth', 'ltc', 'doge', 'bch', 'xrp', 'xlm',
             'ada', 'usdt', 'usdc', 'dai', 'wbtc', 'uniswap', 'sushiswap', 'pancakeswap', 'defi', 'decentralized',
             'finance', 'defi', 'yield', 'farming', 'staking', 'staking', 'pool', 'pooling', 'staking', 'staking',
             'staking', 'join', 'group', 'telegram', 'whatsapp', 'discord', 'discord nitro', 'antivirus', 'free', 'true']

# Function to resolve DNS records in bulk using dns.resolver
def resolve_dns_records(urls):
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1
    resolver.lifetime = 1
    return [resolver.resolve(url, 'A')[0].address for url in urls]

# Function to get IP address
def get_ip(url):
    try:
        ip_address = socket.gethostbyname(url)
        return get_ip(url) if ":" in ip_address else ip_address
    except Exception:
        return ''

# Function to get iframes
def get_iframes(url, soup):
    try:
        iframes = soup.find_all('iframe')
        return iframes
    except Exception:
        return []

# Function to get age
def get_age(url):
    try:
        domain = whois.whois(url)
        if isinstance(domain.creation_date, list):
            delta = datetime.now() - domain.creation_date[0]
        else:
            delta = datetime.now() - domain.creation_date
        age = delta.days
    except Exception:
        return ''
    return age

# Function to check SSL presence
def get_ssl(url):
    try:
        context = ssl.create_default_context()
        with requests.get(f'https://{url}', verify=False, timeout=5) as response:
            ssl_present = response.ok
    except Exception:
        ssl_present = False
    return ssl_present

# Function to get blacklisted words
def get_blacklisted_words(url, webpage_text):
    pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, blacklist)))
    blacklisted_words = re.findall(pattern, webpage_text)
    return blacklisted_words

# Function to get nameserver
def get_nameserver(url):
    try:
        answers = dns.resolver.resolve(url, 'NS')
        nameservers = [rdata.to_text()[:-1] for rdata in answers]
        return f"[{', '.join(nameservers)}]"
    except Exception:
        return ''

# Function to get status code
def get_status_code(url):
    try:
        response = requests.get(f'https://{url}', verify=False, timeout=5)
        if response.status_code != 200:
            response = requests.get(f'http://{url}', verify=False, timeout=5)
        status_code = response.status_code
    except Exception:
        return ''
    return status_code

# Function to process a row
def process_row(row):
    url = row[0]
    ip = get_ip(url)
    iframes = get_iframes(url, row[1])
    age = get_age(url)
    ssl = get_ssl(url)
    blacklisted_words = get_blacklisted_words(url, row[2])
    nameserver = get_nameserver(url)
    blacklisted_words_count = len(blacklisted_words)
    status_code = get_status_code(url)
    length = len(url)
    return [url, ip, iframes, age, ssl, iframes, blacklisted_words, nameserver, blacklisted_words_count, status_code, length]

# Function to print memory usage
def print_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"Memory usage: {memory_info.rss / (1024*1024):.2f} MB")

# Main function
def main():
    # Record the start time
    start_time = time.perf_counter()

    # Read the input CSV file using pandas
    df = pd.read_csv('../Dataset_Files/online-valid-scrapped-cut.csv')

    # Resolve DNS records in bulk
    urls = df['url'].tolist()
    ip_addresses = resolve_dns_records(urls)

    # Create a list of BeautifulSoup objects for each webpage
    webpages = []
    for url in tqdm(urls):
        try:
            response = requests.get(url, verify=False, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            webpages.append(soup)
        except Exception:
            webpages.append(None)

    # Process the rows in parallel using asyncio
    output_data = []
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for index, row in df.iterrows():
            future = loop.run_in_executor(
                executor, process_row, (row, ip_addresses[index], webpages[index])
            )
            futures.append(future)
        for result in tqdm(asyncio.as_completed(futures), total=len(futures)):
            output_data.append(result.result())

    # Record the end time
    end_time = time.perf_counter()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    print(f"Time taken: {elapsed_time:.6f} seconds")
    print_memory_usage()

    # Write the output data to a CSV file using pandas
    df_output = pd.DataFrame(output_data, columns=['url', 'ip_address', 'iframes', 'age', 'ssl', 'iframes',
                                                   'blacklisted_words', 'nameserver', 'blacklisted_words_count',
                                                   'status_code', 'length'])
    df_output.to_csv('../Dataset_Files/Scrapednew.csv', index=False)

if __name__ == "__main__":
    main()
