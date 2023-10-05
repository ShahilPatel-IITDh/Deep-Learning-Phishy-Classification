# object_detection.py

import cv2
import numpy as np

def detect_input_box(screenshot_file_path):
    # Load the screenshot using OpenCV
    screenshot = cv2.imread(screenshot_file_path)

    # Convert the screenshot to grayscale
    grayscale_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Apply image processing (e.g., thresholding) to highlight potential input boxes
    _, thresholded_screenshot = cv2.threshold(grayscale_screenshot, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresholded_screenshot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour resembles an input box
    input_box_detected = False

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)

        # You can adjust these thresholds as needed
        if 0.5 <= aspect_ratio <= 2.0 and 50 <= w <= 300 and 10 <= h <= 100:
            input_box_detected = True
            break

    if input_box_detected:
        return -1  # Input box detected
    else:
        return 1   # Input box not detected
