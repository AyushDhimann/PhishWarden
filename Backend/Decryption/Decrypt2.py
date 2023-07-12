import base64
import json
from Crypto.Cipher import AES

def decrypt_url(encrypted_url):
    custom_key = "1234567890123456"
    key = custom_key.encode('utf-8')
    iv = custom_key.encode('utf-8')
    encrypted = base64.b64decode(encrypted_url)

    aes = AES.new(key, AES.MODE_CBC, iv)
    decrypted = aes.decrypt(encrypted)
    decrypted_url = decrypted.decode('iso-8859-1').strip()

    return decrypted_url
#Read the text from file.txt
with open('../Decryption/file.txt', 'r') as f:
    text = f.read()

# Get only the value of the text (assuming it's the only value in the file)
encrypted_text = text.split(':')[1].strip('{}"')

if __name__ == '__main__':
    import sys
    encrypted_url = encrypted_text
    decrypted_url = decrypt_url(encrypted_url)
    print(decrypted_url)