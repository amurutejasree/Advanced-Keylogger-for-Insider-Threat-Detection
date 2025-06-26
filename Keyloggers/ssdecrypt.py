from cryptography.fernet import Fernet
import os

# Load the encryption key (the same key used to encrypt the data)
with open("encryption_key.key", "rb") as key_file:
    ENCRYPTION_KEY = key_file.read()

# Initialize Fernet for decryption
cipher = Fernet(ENCRYPTION_KEY)

# Function to decrypt the encrypted screenshot
def decrypt_screenshot(encrypted_file_path):
    # Read the encrypted file
    with open(encrypted_file_path, "rb") as ef:
        encrypted_data = ef.read()

    # Decrypt the file data
    decrypted_data = cipher.decrypt(encrypted_data)

    # Save the decrypted file (removing the ".encrypted" extension)
    decrypted_file_path = encrypted_file_path.replace(".encrypted", "")
    with open(decrypted_file_path, "wb") as df:
        df.write(decrypted_data)

    return decrypted_file_path

# Example usage
# Example usage
encrypted_file_path = r"C:/Users/tejas/Downloads/screenshot.encrypted.png"  # Path to the actual encrypted file
decrypted_file_path = decrypt_screenshot(encrypted_file_path)
print(f"Decrypted file saved at: {decrypted_file_path}")
