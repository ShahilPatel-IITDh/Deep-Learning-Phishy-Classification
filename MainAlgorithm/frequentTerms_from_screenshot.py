import pytesseract
from PIL import Image
import cv2
import numpy as np
from collections import Counter
import re

def preprocess_image(image_path):
    # Open the image using OpenCV
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to enhance text
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invert the colors to make text black on a white background
    inverted = cv2.bitwise_not(thresholded)

    # Convert back to a PIL image
    processed_image = Image.fromarray(inverted)

    return processed_image

def extract_top_terms_from_screenshot(domain_name, screenshot_path):
    # Preprocess the image
    processed_image = preprocess_image(screenshot_path)

    # Use Tesseract OCR to extract text from the preprocessed image
    text = pytesseract.image_to_string(processed_image)

    # Tokenize the extracted text by words, removing non-alphabetical characters and numbers
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    # Count the occurrences of each word
    word_counts = Counter(words)

    # Get the top 5 most common terms
    top_terms = word_counts.most_common(5)

    # Extract only the terms (ignore the counts)
    top_terms = [term for term, count in top_terms]

    return top_terms

# Example usage:
# if __name__ == "__main__":
#     domain_name = "example.com"
#     screenshot_path = "path_to_your_screenshot.png"
#     top_terms = extract_top_terms_from_screenshot(domain_name, screenshot_path)
#     print(f"Top 5 most occurring terms for {domain_name}:", top_terms)