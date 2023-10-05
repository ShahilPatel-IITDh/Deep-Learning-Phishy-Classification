# object_detection.py

import cv2
import numpy as np
import pytesseract

def detect_input_box(screenshot_file_path):
    # Load the screenshot using OpenCV
    screenshot = cv2.imread(screenshot_file_path)

    # Convert the screenshot to grayscale
    grayscale_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # # Apply image processing (e.g., thresholding) to highlight potential input boxes
    _, thresholded_screenshot = cv2.threshold(grayscale_screenshot, 200, 255, cv2.THRESH_BINARY)


    # # The code to find input boxes using contours is accurate but slow. Also we need to tune the aspect ratio, width and height of the input box as per our requirements, so that it covers most of the webpages.

    # # This requires investment of time and effort. I have also provided a quick and simple way to check if an input box is present in the screenshot. You can uncomment and use the code below if you want to quickly check if an input box is present in the screenshot.

    # # Find contours in the thresholded image
    # contours, _ = cv2.findContours(thresholded_screenshot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # # Check if any contour resembles an input box
    # input_box_detected = False

    # for contour in contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     aspect_ratio = w / float(h)

    #     # Adjust the ratios as per your requirements
    #     if 0.5 <= aspect_ratio <= 2.0 and 50 <= w <= 300 and 10 <= h <= 100:
    #         input_box_detected = True
    #         break

    # if input_box_detected:
    #     return -1  # Input box detected
    
    # else:
    #     return 1   # Input box not detected
    

    # For quick and simple checking use the code below
    
    # Use Tesseract OCR to extract text from the screenshot
    extracted_text = pytesseract.image_to_string(thresholded_screenshot)

    # Check if the extracted text contains keywords indicating input boxes
    keywords = ["username", "Username", "USERNAME","password", "Password" ,"email", "Email", "e-mail", "E-mail","input", "Input", "textbox", "form", "signin", "Signin", "sign-in", "Sign-in", "login", "Login", "log-in", "Log-in"]

    for keyword in keywords:
        if keyword in extracted_text.lower():

            return -1  # Input box detected

    return 1  # Input box not detected