from cryptography.fernet import Fernet

# Load the encryption key (the same key used to encrypt the data)
with open("encryption_key.key", "rb") as key_file:
    encryption_key = key_file.read()

# Initialize Fernet with the encryption key
cipher = Fernet(encryption_key)

# Example encrypted message (this should be the encrypted string you received via email)
encrypted_message = b"gAAAAABnKMjuLK81KJx4joP0pdcLYztzVeISZjU4LTh6qeKKT0DZLWX8QiIUwJCD10drixOtEQyVHLzYEV0-gVnadwRKLDs0vGXgCXpQZyvhu3ruZIxN9ZA="

# Decrypt the message
try:
    decrypted_message = cipher.decrypt(encrypted_message)
    print("Decrypted Message:", decrypted_message.decode('utf-8'))
except Exception as e:
    print(f"Decryption failed: {e}")