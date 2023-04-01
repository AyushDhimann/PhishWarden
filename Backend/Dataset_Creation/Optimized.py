# pip install bs4 pythondns dnspython Levenshtein requests tqdm python-whois urllib3

from bs4 import BeautifulSoup
import csv
from datetime import datetime
import dns.resolver
import requests
import threading
import time
import ssl
import subprocess
import whois
import urllib3

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


# Functions

def get_ip(url):
    try:
        ip_address = requests.get(f'http://ip-api.com/json/{url}').json().get('query')
    except Exception:
        ip_address = ''
    return ip_address


def get_length(url):
    try:
        length_url = len(url)
    except Exception:
        length_url = ''
    return length_url


def get_ssl(url):
    try:
        context = ssl.create_default_context()
        with requests.get(f'https://{url}', verify=False, timeout=5) as response:
            ssl_present = response.ok
    except Exception:
        ssl_present = False
    return ssl_present


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


def get_nameserver(url):
    try:
        domain = url  # [4:]
        answers = dns.resolver.resolve(domain, 'NS')
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


def get_status_code(url):
    try:
        response = requests.get(f'https://{url}', verify=False, timeout=5)
        if response.status_code != 200:
            response = requests.get(f'http://{url}', verify=False, timeout=5)
        status_code = response.status_code
    except Exception:
        status_code = ''
    return status_code


def get_blacklisted_words(url):
    try:
        response = requests.get(url)
        webpage_text = response.text
        blacklisted_words = [word for word in blacklist if word in webpage_text]

    except Exception:
        blacklisted_words = ''
    return blacklisted_words


def get_blacklisted_words_count(url):
    try:
        response = requests.get(url)
        webpage_text = response.text
        blacklisted_words = [word for word in blacklist if word in webpage_text]

    except Exception:
        blacklisted_words = ''
    return len(blacklisted_words)


# def get_blacklisted_words_ratio(url):
#     global webpage_text
#     webpage_text = ''
#     try:
#         response = requests.get(url)
#         webpage_text = response.text
#         blacklisted_words = [word for word in blacklist if word in webpage_text]
#
#     except Exception:
#         blacklisted_words = ''
#     return len(blacklisted_words) / len(webpage_text)


def get_iframes(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        iframes = soup.find_all('iframe')

    except Exception:
        iframes = '0'
    return iframes


with open('input.csv', mode='r') as csv_file:
    # Create a new thread to process the URL
    thread = threading.Thread(target=process_url, args=(url,))
    threads.append(thread)
    # Start the thread
    thread.start()
    csv_reader = csv.reader(csv_file)
    output_data = []
    reader = csv.reader(csv_file)
    for row in csv_reader:
        url = row[0]
        get_ip(url)
        get_iframes(url)
        get_age(url)
        get_ssl(url)
        get_iframes(url)
        get_nameserver(url)
        get_blacklisted_words(url)
        get_blacklisted_words_count(url)
        #get_blacklisted_words_ratio(url)
        get_status_code(url)
        get_length(url)
        output_data.append([url, get_ip(url), get_iframes(url), get_age(url), get_ssl(url), get_iframes(url), get_blacklisted_words(url), get_nameserver(url), get_blacklisted_words_count(url), get_status_code(url), get_length(url)])
        print([url, get_ip(url), get_iframes(url), get_age(url), get_ssl(url), get_iframes(url), get_blacklisted_words(url), get_nameserver(url), get_blacklisted_words_count(url), get_status_code(url), get_length(url)])

with open('optoutput.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(output_data)