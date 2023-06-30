import csv
import tldextract

with open('phish-cut.csv', mode='r') as urls_file:
    csv_reader = csv.reader(urls_file)
    urls = [row[0] for row in csv_reader]

modified_urls = []
for url in urls:
    # Remove "https://" prefix
    url = url.replace('https://', '')

    # Extract domain and TLD using tldextract
    extracted = tldextract.extract(url)
    domain = extracted.domain
    subdomain = extracted.subdomain
    print(tldextract.extract(url))
    tld = extracted.suffix

    # Combine domain and TLD to form new URL
    new_url = f'{subdomain}.{domain}.{tld}'

    modified_urls.append(new_url)

with open('modified_phish.csv', mode='w', newline='') as modified_urls_file:
    urls_writer = csv.writer(modified_urls_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    urls_writer.writerow(['URLs'])
    for url in modified_urls:
        urls_writer.writerow([url])