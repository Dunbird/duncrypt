from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import zstandard as zstd

def decompress_file(compressed_data):
    dctx = zstd.ZstdDecompressor()
    decrompressed_data = dctx.decompress(compressed_data)
    return decrompressed_data

def decrypt_file(encrypted_file_path, key, output_file_path):
    with open(encrypted_file_path, 'rb') as f:
        iv = f.read(12)
        file_content = f.read()
        encrypted_data = file_content[:-16]
        tag  = file_content[-16:]
#        I would not recommend printing the key, iv, and tag in a production environment, but it is useful for debugging
#        print(f"IV: {iv.hex()} Length: {len(iv)}")
#        print(f"Tag: {tag.hex()} Length: {len(tag)}")
#        print(f"Key: {key.hex()} Length: {len(key)}")

    
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    decompressed_data = decompress_file(decrypted_data)

    with open(output_file_path, 'wb') as out_file:
        out_file.write(decompressed_data)
    print(f"File decrupted and saved as {output_file_path}")

if __name__ == "__main__":
    encrypted_file_path = input("Enter the path to the encrypted .dun file: ")
    output_file_path = input("Enter the output file path for the decryped file: ")

    image_path = input("enter the key image: ")
    from image_process import derive_key_from_image
    key = derive_key_from_image(image_path)

    decrypt_file(encrypted_file_path, key, output_file_path)

