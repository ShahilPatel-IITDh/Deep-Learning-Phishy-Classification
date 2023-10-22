import pytesseract
from PIL import Image
import cv2
import numpy as np
from collections import Counter
import re

# Define a list of common stopwords
stopwords = ["a", "an", "the", "me", "you", "we", "they", "it", "he", "she", "is", "am", "are", "was", "were", "his", "her", "your"]


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

    print("Code entered the extract_top_terms_from_screenshot function")
    
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

    print("Code is about to exit the extract_top_terms_from_screenshot function")

    return top_terms