import cv2
import numpy as np
import pyautogui
import time
import os
from cryptography.fernet import Fernet

# Generate an encryption key (do this only once and save it securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Save the key to a file (do this only once, and use the same key for decryption)
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)

def record_and_encrypt_screen(duration=10, fps=10):
    frame_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # MP4 encoding

    # Paths for the original and encrypted files
    temp_video_path = "temp_screen_recording.mp4"
    encrypted_video_path = "encrypted_screen_recording.mp4"
    out = cv2.VideoWriter(temp_video_path, fourcc, fps, (frame_size.width, frame_size.height))

    start_time = time.time()
    while time.time() - start_time < duration:
        img = pyautogui.screenshot()  # Capture a screenshot
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB

        out.write(frame)  # Write frame to video

        time.sleep(1 / fps)  # Control frame rate

    out.release()

    # Encrypt the video file
    with open(temp_video_path, "rb") as f:
        file_data = f.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    with open(encrypted_video_path, "wb") as f:
        f.write(encrypted_data)

    # Remove the temporary unencrypted file
    os.remove(temp_video_path)
    print("Screen recording encrypted and saved.")

# Run the encryption process
record_and_encrypt_screen(duration=10, fps=10)
