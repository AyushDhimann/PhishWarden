import base64
from Crypto.Cipher import AES

# Read the text from file.txt
with open('file.txt', 'r') as f:
    text = f.read()

# Get only the value of the text (assuming it's the only value in the file)
encrypted_text = text.split(':')[1].strip('{}"')

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

# Get the domain name from the decrypted text
# domain_name = decrypted_text.split('\x01')[1]
print(decrypted_text)
print(len(decrypted_text))
domain_name = decrypted_text[32:-3]

# Print the domain name
print(domain_name)
