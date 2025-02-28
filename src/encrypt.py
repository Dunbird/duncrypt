import os
import struct
import zstandard as zstd
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import glob



def encrypt_file(input_file_path, key, output_path):
    with open(input_file_path, 'rb') as f:
        file_data = f.read()


    cctx = zstd.ZstdCompressor()
    compressed_data = cctx.compress(file_data)

    iv = os.urandom(12)

    original_filename = os.path.basename(input_file_path)
    filename_bytes = original_filename.encode()
    filename_length = len(filename_bytes)

    file_metadata = struct.pack(f"B{filename_length}s", filename_length, filename_bytes)

    pre_encryptdata = file_metadata + compressed_data


    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(pre_encryptdata) + encryptor.finalize()

    encrypted_file_data = iv + encrypted_data + encryptor.tag

    with open(output_path, 'wb') as f:
        f.write(encrypted_file_data)
#        I would not recommend printing the key, iv, and tag in a production environment, but it is useful for debugging
#        print(f"IV: {iv.hex()} Length: {len(iv)}")
#        print(f"Tag: {encryptor.tag.hex()} Length: {len(encryptor.tag)}")
#        print(f"Key: {key.hex()} Length: {len(key)}")

    print(f"File encrypted and saved as {output_path}")


def main():
    print("Encryption Modes available: Manual, Directory")
    mode = input("What mode would you like to continue with? ")
    
    if mode.lower() in ("man", "manual"):
        file_path = input("Enter the path the the file to encrypt: ")
        if file_path.endswith(".dun"):
            print("Skipping files already encrypted.")
            return
        
        encoutput_path = file_path + '.dun'

        image_path = input("Enter the path to the image being used for encryption: ").strip()
        from image_process import derive_key_from_image
        key = derive_key_from_image(image_path)

        encrypt_file(file_path, key, encoutput_path) 

    elif mode.lower() in ('dir','directory'):
        directory = input("Input the directory holding the files you want to encrypt: ").strip()
        if not os.path.exists(directory):
            print(f"{directory} is not a valid directory.")
            return
        files = glob.glob(os.path.join(directory, '*'))
        if not files:
            print(f'No files were found in {directory}')
            return
        image_path = input("Enter the path to the image being used for encryption").strip()
        from image_process import derive_key_from_image
        key = derive_key_from_image(image_path)

        for file_path in files:
            if os.path.isfile(file_path) and not file_path.endswith(".dun"):
                encoutput_path = file_path + ".dun"
                try:
                    encrypt_file(file_path,key,encoutput_path)
                except Exception as e:
                    print(f'Error encrypting {file_path}: {e}')
    else:
        print(f"{mode} is an invalid mode.")


if __name__ == "__main__":
    main()
