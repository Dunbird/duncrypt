from PIL import Image
import numpy as np
import hashlib
# Loads user provided image > converts to grayscale > resizes to 256x256 > normalizes pixel values into array ...
# flattens the array > converts values to bytes
def process_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.resize((256, 256))
    img_array = np.array(img) / 255.0
    pixel_data = img_array.flatten().tobytes()
    return pixel_data
# creates key from image data using SHA-256 and returns it as a binary output
def derive_key_from_image(image_path):
    pixel_data = process_image(image_path)
    key = hashlib.sha256(pixel_data).digest()
    return key

if __name__ == "__main__":
    image_path = input("Enter the path to the image being used as the key: ")
    key = derive_key_from_image(image_path)
    print(f"Derived key (SHA-256): {key.hex()}")
