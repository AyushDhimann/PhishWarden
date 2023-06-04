from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
customKey="1234567890123456"
txttobeencrypted="chat.forefront.ai"
def encrypt_data(txttobeencrypted):
    # Encoding the Key
    key = customKey.encode()

    # Encrypt the plaintext with AES-CBC
    iv = customKey.encode()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(txttobeencrypted.encode()) + padder.finalize()
    encryptedData = encryptor.update(padded_data) + encryptor.finalize()

    # Concatenate the key and IV to the encrypted data
    encrypted = key + iv + encryptedData

    # Convert the encrypted data to a base64-encoded string
    base64Encrypted = base64.b64encode(encrypted).decode()

    # Return the encrypted data
    return base64Encrypted

print(encrypt_data(txttobeencrypted))
