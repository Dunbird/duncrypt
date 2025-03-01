# DunCrypt

DunCrypt is a file encryption and decryption tool that allows users to securely encrypt files using a key derived from an image. After encrytion files are compressed and then saved as a custom `.dun` file.

## Features
- Encrypt individual files or all files in a directory
- Decrypt individual files or all `.dun` files in a directory
- Uses AES-256-GCM encryption
- Compresses files using Zstandard (zstd) before encryption
- Stores original filename metadata in the encrypted file header
- Derives encryption key from an image

## Installation
Ensure you have Python 3 installed, then install the required dependencies:
```sh
pip install cryptography zstandard
```

## Usage
### Encryption
To encrypt a single file or all files within a directory:
```sh
python encrypt.py
```
Follow the prompts to select the encryption mode, file, output name, and image for key derivation.

### Decryption
To decrypt a single or all files within a directory:
```sh
python decrypt.py
```
Choose the encryption mode then provide, output directory, and the image used for encryption.

## File Format
Encrypted files (`.dun`) include:
1. IV (12 bytes)
2. Encrypted data (including compressed content and metadata)
3. Authentication tag (16 bytes)

The metadata contains the original filename and extension, allowing automatic reconstruction during decryption.

## Notes
- Do not lose the image used for encryption, as it is required for decryption.
- The tool will skip encrypting `.dun` files to prevent double encryption.
- Debugging messages are disabled for security but can be re-enabled if needed.

## Upcoming Features
- **GUI Support** - A graphical interface for easier encryption and decryption.
- **Web-based Version** - Integrate DunCrypt into a web frontend for broader accessibility.
- **Multiple Image Key Support** - Option to combine multiple images for key derivation.





## License
MIT License

## Author
Dunbird (Carlos)

