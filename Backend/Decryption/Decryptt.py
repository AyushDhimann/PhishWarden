import base64
from Crypto.Cipher import AES

# Define the encrypted text and key
encrypted_text = 'MTIzNDU2Nzg5MDEyMzQ1NjEyMzQ1Njc4OTAxMjM0NTa795HYj+4S+4lW/R98d7Bf' + '=='
key = b'1234567890123456'
iv = b'1234567890123456'

# Convert the encrypted text from Base64 to bytes
encrypted_bytes = base64.b64decode(encrypted_text)

# Create the AES cipher object
cipher = AES.new(key, AES.MODE_CBC, iv=iv) # Use CBC mode and pass the IV

# Decrypt the text
decrypted_bytes = cipher.decrypt(encrypted_bytes)

# Print the decrypted bytes as hex
print(decrypted_bytes.hex())

# Try decoding the decrypted bytes to a different encoding
try:
    decrypted_text = decrypted_bytes.decode('iso-8859-1')
    print(decrypted_text)
except UnicodeDecodeError:
    print("Unable to decode decrypted bytes")
