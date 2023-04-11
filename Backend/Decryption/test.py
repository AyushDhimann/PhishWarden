import re

text = "\x15\x93\xa8|\xcf\x9cg\xc5J+\xf3\x80\x16\xaa\x01\x15\x93\xa8|\xcf\x9cg\xc5J+\xf3\x80\x16\xaa\x01https://github.com\x06\x06\x06\x06\x06\x06"

# Define a regular expression pattern to match URLs
url_pattern = re.compile(r'(https?://[^\s]+)')

# Search for the first match of the URL pattern in the text
match = url_pattern.search(text)

# If a match was found, extract the URL
if match:
    url = match.group(1)
    domain = url.split('//')[1].split('/')[0]
    print(domain)
else:
    print("No URL found in text")
