from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import zstandard as zstd

def compress_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    cctx = zstd.ZstdCompressor()
    compressed_data =cctx.compress(data)
    return compressed_data

def encrypt_file(file_path, key, output_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()

    compressed_data = compress_file(file_path)


    iv = os.urandom(12)

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(compressed_data) + encryptor.finalize()

    with open(output_path, 'wb') as output_file:
        output_file.write(iv)
        output_file.write(encrypted_data)
        output_file.write(encryptor.tag)
    print(f"File encrypted and saved as {output_file}")


if __name__ == "__main__":
    file_path = input("Enter the path to the file to encrypt: ")
    output_path = input("Enter the output file path ('filename'.dun): ")

    image_path = input("Enter the image path to derive key: ")
    from image_process import derive_key_from_image
    key = derive_key_from_image(image_path)

    encrypt_file(file_path, key, output_path)
