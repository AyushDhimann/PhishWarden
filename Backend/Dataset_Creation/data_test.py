import concurrent.futures
import pandas as pd
import requests
import socket
import ssl
import time
from tqdm import tqdm
import urllib3

urllib3.disable_warnings()

blacklist = ['snapchat', 'linkedin', 'youtube', 'whatsapp', 'gmail', 'yahoo', 'outlook', 'hotmail', 'aol', 'icloud', 'instant', 'bitcoin', 'litecoin', 'ethereum', 'dogecoin', 'binance', 'coinbase', 'coinmarketcap', 'cryptocurrency', 'cryptocurrencies', 'crypto', 'currency', 'blockchain', 'btc', 'eth', 'ltc', 'doge', 'bch', 'xrp', 'xlm', 'ada', 'usdt', 'usdc', 'dai', 'wbtc', 'uniswap', 'sushiswap', 'pancakeswap', 'defi', 'decentralized', 'finance', 'defi', 'yield', 'farming', 'staking', 'staking', 'pool', 'pooling', 'staking', 'staking', 'staking', 'join', 'group', 'telegram', 'whatsapp', 'discord', 'discord nitro', 'antivirus', 'free', 'true']

def get_ip(url):
    try:
        ip_address = socket.gethostbyname(url)
        return get_ip(url) if ":" in ip_address else ip_address
    except Exception:
        return ''

def get_iframes(url):
    try:
        response = requests.get(url, verify=False, timeout=5)
        webpage_text = response.text.lower()
        blacklisted_words = [word for word in blacklist if f' {word} ' in f' {webpage_text} ']
        return blacklisted_words
    except Exception:
        return []

def get_nameserver(url):
    try:
        answers = dns.resolver.resolve(url, 'NS')
        nsdata = [rdata.to_text()[:-1] for rdata in answers]
        return f'[{", ".join(nsdata)}]'
    except Exception:
        return ''

def get_blacklisted_words_count(url):
    blacklisted_words = get_iframes(url)
    return len(blacklisted_words)

def get_status_code(url):
    try:
        session = requests.Session()
        response = session.get(f'https://{url}', verify=False, timeout=5)
        if response.status_code != 200:
            response = session.get(f'http://{url}', verify=False, timeout=5)
        return response.status_code
    except Exception:
        return ''

def get_length(url):
    try:
        return len(url)
    except Exception:
        return ''

def process_row(row):
    url = row[0]
    ip = get_ip(url)
    iframes = get_iframes(url)
    nameserver = get_nameserver(url)
    blacklisted_words_count = get_blacklisted_words_count(url)
    status_code = get_status_code(url)
    length = get_length(url)
    return [url, ip, iframes, nameserver, blacklisted_words_count, status_code, length]

# Read the input CSV file using pandas
df = pd.read_csv('../Dataset_Files/online-valid-scrapped-cut.csv')

# Process the rows in parallel using a ThreadPoolExecutor
output_data = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for index, row in df.iterrows():
        future = executor.submit(process_row, row)
        futures.append(future)
    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
        result = future.result()
        output_data.append(result)

# Write the output data to a CSV file using pandas
df_output = pd.DataFrame(output_data, columns=['url', 'ip_address', 'iframes', 'nameserver', 'blacklisted_words_count', 'status_code', 'length'])
df_output.to_csv('../Dataset_Files/Scrapednew.csv', index=False)
