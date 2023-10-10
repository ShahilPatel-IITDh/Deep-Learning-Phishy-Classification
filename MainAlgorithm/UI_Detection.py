# object_detection.py

import cv2
import numpy as np
import pytesseract

def detect_input_box(screenshot_file_path):
    # Load the screenshot using OpenCV
    screenshot = cv2.imread(screenshot_file_path)

    # Convert the screenshot to grayscale
    grayscale_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Apply image processing (e.g., thresholding) to highlight potential input boxes
    _, thresholded_screenshot = cv2.threshold(grayscale_screenshot, 200, 255, cv2.THRESH_BINARY)

    # For quick and simple checking use the code below
        
    # Use Tesseract OCR to extract text from the screenshot
    extracted_text = pytesseract.image_to_string(thresholded_screenshot)

    # Check if the extracted text contains keywords indicating input boxes
    keywords = ["username", "Username", "USERNAME","password", "Password" ,"email", "Email", "e-mail", "E-mail","input", "Input", "textbox", "form", "signin", "Signin", "sign-in", "Sign-in", "login", "Login", "log-in", "Log-in"]

    for keyword in keywords:
        if keyword in extracted_text.lower():
            return -1  # Input box detected

    return 1  # Input box not detected