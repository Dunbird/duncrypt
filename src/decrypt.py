from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import zstandard as zstd
import glob
import struct


def decrypt_file(encrypted_file_path, key, output_directory):
    if not encrypted_file_path.endswith('.dun'):
        print(f'Skipping non-encrypred file: {encrypted_file_path}')
        return

    with open(encrypted_file_path, 'rb') as f:
        file_contents = f.read()
    iv = file_contents[:12]
    encrypted_data = file_contents[12:-16]
    tag  = file_contents[-16:]
#        I would not recommend printing the key, iv, and tag in a production environment, but it is useful for debugging
#        print(f"IV: {iv.hex()} Length: {len(iv)}")
#        print(f"Tag: {tag.hex()} Length: {len(tag)}")
#        print(f"Key: {key.hex()} Length: {len(key)}")
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    except Exception as e:
            print(f'Failed to decrypt {encrypted_file_path}: {e}')
            return
    
    filename_length = decrypted_data[0]
    filename_bytes = decrypted_data[1:filename_length + 1]
    original_filename = filename_bytes.decode()

    compressed_data = decrypted_data[filename_length +1:]

    dctx = zstd.ZstdDecompressor()
    decompressed_data = dctx.decompress(compressed_data)

    output_file_path = os.path.join(output_directory, original_filename)
    with open(output_file_path, 'wb') as f:
        f.write(decompressed_data)
    print(f"File decrypted and saved as {output_file_path}")

def main():
    print("Decryption Modes: Manual , Directory")
    mode = input("What mode would you like to continue with? ").strip()


    if mode.lower() in ('manual', 'man'):
        file_path = input("Enter the path to the encrypted .dun file: ")
        if not file_path.endswith('.dun'):
            print('Invalid file type. Only .dun files can be decrypted')
            return
        
        output_directory = input("Enter the output file path for the decryped file: ")
        os.makedirs(output_directory, exist_ok=True)

        image_path = input("Enter the key image: ")
        from image_process import derive_key_from_image
        key = derive_key_from_image(image_path)
        decrypt_file(file_path, key, output_directory)


    elif mode.lower() in ('directory', 'dir'):
        directory = input('Enter the Directory containing .dun files: ').strip()
        if not os.path.exists(directory):
            print("Invalid directory.")
            return

        dun_files = glob.glob(os.path.join(directory, "*.dun"))
        if not dun_files:
             print('There are no .dun files in specified directory')
             return
        
        output_directory = input("Enter the output directory: ").strip()
        os.makedirs(output_directory, exist_ok=True)
        image_path = input('Enter the path to the image used for decryption: ').strip()
        from image_process import derive_key_from_image
        key = derive_key_from_image(image_path)

        for dun_file in dun_files:
            if os.path.isfile(dun_file):
                try:
                    decrypt_file(dun_file, key, output_directory)
                except Exception as e:
                    print(f"there was an error decrypting {dun_file}: {e}")
    else:
        print(f'{mode} is an invalid mode')



if __name__ == "__main__":
    main()
