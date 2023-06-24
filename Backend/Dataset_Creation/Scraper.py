import time
import psutil
import requests
import socket
from bs4 import BeautifulSoup
from datetime import datetime
import dns.resolver
import ssl
import whois
import urllib3
import sys
sys.path.append('../Decryption/')
import Decrypt

urllib3.disable_warnings()

blacklist = ['spam', 'scam', 'fraud', 'phishing', 'gift', 'surprise', 'real', 'legit', 'trusted', 'seller', 'buyer',
             'fast', 'secure', 'login', 'verify', 'account', 'update', 'confirm', 'bank', 'paypal', 'ebay', 'amazon',
             'ebay', 'apple', 'microsoft', 'google', 'facebook', 'instagram', 'twitter', 'snapchat', 'linkedin',
             'youtube', 'whatsapp', 'gmail', 'yahoo', 'outlook', 'hotmail', 'aol', 'icloud', 'instant' 'bitcoin',
             'litecoin', 'ethereum', 'dogecoin', 'binance', 'coinbase', 'coinmarketcap', 'cryptocurrency',
             'cryptocurrencies', 'crypto', 'currency', 'blockchain', 'btc', 'eth', 'ltc', 'doge', 'bch', 'xrp', 'xlm',
             'ada', 'usdt', 'usdc', 'dai', 'wbtc', 'uniswap', 'sushiswap', 'pancakeswap', 'defi', 'decentralized',
             'finance', 'defi', 'yield', 'farming', 'staking', 'staking', 'pool', 'pooling', 'staking', 'staking',
             'staking', 'join', 'group', 'telegram', 'whatsapp', 'discord', 'discord nitro', 'antivirus']

blacklisted_words=[]

# Record the start time
start_time = time.perf_counter()

def print_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"Memory usage: {memory_info.rss / (1024*1024):.2f} MB")

print_memory_usage()

def get_ip(url):
    print(url)
    try:
        ip_address = socket.gethostbyname(url)
        return get_ip(url) if ":" in ip_address else ip_address
    except Exception:
        ip_address = ''
    print("IP is : ",ip_address)
    return ip_address


def get_iframes(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        iframes = soup.find_all('iframe')

    except Exception:
        iframes = '0'
    print("iframes is : ", iframes)
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
    print("age is : ", age)
    return age

def get_ssl(url):
    try:
        context = ssl.create_default_context()
        with requests.get(f'https://{url}', verify=False, timeout=5) as response:
            ssl_present = response.ok
    except Exception:
        ssl_present = False
    print("ssl_present is : ", ssl_present)
    return ssl_present


import requests
import dns.resolver

def get_blacklisted_words(url):
    try:
        response = requests.get(url)
        webpage_text = response.text.lower()
        blacklisted_words = [word for word in blacklist if f' {word} ' in f' {webpage_text} ']

    except Exception:
        blacklisted_words = ''
    return blacklisted_words


def get_nameserver(url):
    try:
        answers = dns.resolver.resolve(url, 'NS')
        nsdata = []
        for rdata in answers:
            data = rdata.to_text()
            nsdata.append(data[:-1])
        output_list = [line.strip() for line in nsdata]

        output_str = ''.join(
            output_list[i] if i == 0 else f', {output_list[i]}'
            for i in range(len(output_list))
        )
        nameservers = f'[{output_str}]'

    except Exception:
        nameservers = ''
    return nameservers

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
def process_row(url):
    ip = get_ip(url)
    iframes = get_iframes(url)
    age = get_age(url)
    ssl = get_ssl(url)
    blacklisted_words = get_blacklisted_words(url)
    nameserver = get_nameserver(url)
    blacklisted_words_count = get_blacklisted_words_count(url)
    status_code = get_status_code(url)
    length = get_length(url)
    print(url, ip, iframes, age, ssl, iframes, blacklisted_words, nameserver, blacklisted_words_count, status_code, length)

# with open('../Dataset_Files/url.txt', 'r') as urlfile:
#     url=urlfile.readline()
# print(url)

url = "www.google.com"

# process the rows in parallel using a ThreadPoolExecutor
output_data = []
process_row(url)

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     futures = []
#     for index, row in df.iterrows():
#         future = executor.submit(process_row, row)
#         futures.append(future)
#     for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
#         result = future.result()
#         output_data.append(result)
#         #print(result)


# Record the end time
end_time = time.perf_counter()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print(f"Time taken: {elapsed_time:.6f} seconds")

print_memory_usage()

# write the output data to a CSV file using pandas
# df_output = pd.DataFrame(output_data, columns=['url', 'ip_address', 'iframes', 'age', 'ssl', 'iframes', 'blacklisted_words', 'nameserver', 'blacklisted_words_count', 'status_code', 'length'])
# df_output.to_csv('../Dataset_Files/Scraped.csv', index=False)
#urlfile.close()