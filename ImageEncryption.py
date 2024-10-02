from PIL import Image
import numpy as np
import os

def ensure_file_extension(file_path, default_extension='.png'):
    """Ensure the file path has a valid image extension."""
    root, ext = os.path.splitext(file_path)
    if not ext:
        return file_path + default_extension
    return file_path

def encrypt_decrypt_image(input_path, output_path, key, mode='encrypt'):
    try:
        # Check if the input file exists
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Ensure output path has a valid extension
        output_path = ensure_file_extension(output_path)

        # Open the image
        img = Image.open(input_path)
        
        # Convert image to numpy array
        img_array = np.array(img)
        
        # Flatten the key to handle multi-dimensional arrays
        key_array = np.array([ord(c) for c in key], dtype=np.uint8)
        key_array = np.tile(key_array, img_array.size // len(key_array) + 1)[:img_array.size]
        key_array = key_array.reshape(img_array.shape)
        
        # Perform XOR operation
        result_array = img_array ^ key_array
        
        # Create a new image from the result array
        result_img = Image.fromarray(result_array.astype(np.uint8))
        
        # Save the result image
        result_img.save(output_path)
        print(f"Image {'encrypted' if mode == 'encrypt' else 'decrypted'} and saved as {output_path}")
    except PermissionError:
        print(f"Permission denied. Make sure you have the necessary permissions to access {input_path}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        mode = input("Enter 'e' for encrypt, 'd' for decrypt, or 'q' to quit: ").lower()
        
        if mode == 'q':
            break
        
        if mode not in ['e', 'd']:
            print("Invalid mode. Please try again.")
            continue
        
        input_path = input("Enter the full path to the input image (including file name and extension): ")
        if not os.path.isfile(input_path):
            print("Input file does not exist or is not a file. Please try again.")
            continue
        
        output_path = input("Enter the full path for the output image (including file name and extension): ")
        key = input("Enter the encryption/decryption key: ")
        
        encrypt_decrypt_image(input_path, output_path, key, 'encrypt' if mode == 'e' else 'decrypt')

if __name__ == "__main__":
    main()