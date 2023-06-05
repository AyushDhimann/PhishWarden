import base64
from Crypto.Cipher import AES
import re

#Read the text from file.txt
with open('file.txt', 'r') as f:
    text = f.read()

# Get only the value of the text (assuming it's the only value in the file)
encrypted_text = text.split(':')[1].strip('{}"')
print()
print("Encrypted Text : ",encrypted_text)
print()
f.close()

# Define the key and IV
key = b'1234567890123456'
iv = b'1234567890123456'

# Convert the encrypted text from Base64 to bytes
encrypted_bytes = base64.b64decode(encrypted_text)

# Create the AES cipher object
cipher = AES.new(key, AES.MODE_CBC, iv=iv) # Use CBC mode and pass the IV

# Decrypt the text
decrypted_bytes = cipher.decrypt(encrypted_bytes)

# Strip null bytes and convert to string
decrypted_text = decrypted_bytes.rstrip(b'\0').decode('iso-8859-1')
print(decrypted_text)
# Get the domain name from the decrypted text
domain_name = decrypted_text[32:]
val=domain_name[-1]
domain_name = re.sub(val, '', domain_name)

# Print the domain name
print(domain_name)

with open('url.txt', 'w') as url:
    url.writelines(domain_name)
url.close()
