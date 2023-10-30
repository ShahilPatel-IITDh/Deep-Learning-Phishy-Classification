"""
Top Terms Extraction from Screenshot Documentation

This Python code is used to extract the top terms (words) from a screenshot of a webpage or document.
The code preprocesses the image, extracts text using Tesseract OCR, tokenizes the text, filters out stopwords,
and returns the top 5 most common terms in the extracted text.

Usage:
To use this script, call the 'extract_top_terms_from_screenshot' function with the following parameters:
- domain_name: The domain name associated with the screenshot (optional).
- screenshot_path: The file path of the screenshot image.

Example:
top_terms = extract_top_terms_from_screenshot("example.com", "screenshot.png")

Dependencies:
- Python 3.x
- The 'pytesseract' library for optical character recognition.
- The 'PIL' (Pillow) library for image processing.
- The 'cv2' (OpenCV) library for image manipulation.
- The 'numpy' library for numerical operations.
- The 'collections' library for counting word occurrences.
- The 're' module for regular expression matching.

Functions:
1. preprocess_image(image_path)
    - image_path: The path of the image to be preprocessed.
    - Returns: A preprocessed PIL image with enhanced text.

2. extract_top_terms_from_screenshot(domain_name, screenshot_path)
    - domain_name: The domain name associated with the screenshot (optional).
    - screenshot_path: The file path of the screenshot image.
    - Returns: A list of the top 5 most common terms (words) in the screenshot.

The code performs several image processing steps, OCR text extraction, and term analysis to identify the most common terms
in the screenshot text. The results are returned as a list of top terms.

Note:
- Ensure that the required libraries are installed before using this script.
- The 'stopwords' list can be customized to include or exclude specific words that you want to filter out from the text.
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from collections import Counter
import re

# Define a list of common stopwords
stopwords = ["a", "an", "the", "me", "you", "we", "they", "it", "he", "she", "is", "am", "are", "was", "were", "his", "her", "your", "and", "also", "or", "not", "ours", "our", "their", "this", "that", "these", "mine", "in", "on", "at", "by", "for", "with", "about", "as", "if", "of", "from", "to", "up", "down", "under", "over", "between", "through", "after", "before", "while", "throughout", "since", "during", "until", "unless", "although", "because", "unless", "without", "throughout", "above", "below", "inside", "outside", "between", "among", "around", "before", "after", "along", "beside", "beneath", "across", "against", "toward", "besides", "into", "onto", "underneath", "upon", "within", "beyond", "inside", "outside", "near", "around"]


def preprocess_image(image_path):
    
    """
    Preprocess the input image for text extraction.

    :param image_path: The path of the image to be preprocessed.
    
    :return: A preprocessed PIL image with enhanced text.
    """

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

    """
    Extract the top 5 terms from a screenshot using OCR and text analysis.

    :param domain_name: The domain name associated with the screenshot (optional).
    :param screenshot_path: The file path of the screenshot image.

    :return: A list of the top 5 most common terms (words) in the screenshot.
    """

    print("--Code entered the extract_top_terms_from_screenshot function")
    print("|")
    
    # Preprocess the image
    processed_image = preprocess_image(screenshot_path)

    # Use Tesseract OCR to extract text from the preprocessed image
    text = pytesseract.image_to_string(processed_image)

    # Tokenize the extracted text by words, removing non-alphabetical characters and numbers
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    # Filter out stopwords from the list of words
    words = [word for word in words if word not in stopwords]

    # Count the occurrences of each word
    word_counts = Counter(words)

    # Get the top 5 most common terms
    top_terms = word_counts.most_common(5)

    # Extract only the terms (ignore the counts)
    top_terms = [term for term, count in top_terms]

    print("|")
    print("--Code is about to exit the extract_top_terms_from_screenshot function\n")

    return top_terms