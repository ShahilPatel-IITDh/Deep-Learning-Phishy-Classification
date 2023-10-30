"""
Top Terms Extraction from Website Documentation

This Python code is used to extract the top terms (words) from the text content of a website. It sends a GET request to
the specified URL, retrieves the web page's HTML content, and extracts text, excluding HTML tags. The extracted text is then
tokenized into words, filtered to remove stopwords, and the most common terms are identified and returned.

Usage:
To use this script, call the 'get_top_terms_from_website' function with the following parameter:
- url: The URL of the website from which you want to extract top terms.

Example:
top_terms = get_top_terms_from_website("https://example.com")

Dependencies:
- Python 3.x
- The 'requests' library for sending HTTP requests.
- The 'BeautifulSoup' library for parsing HTML content.
- The 'collections' library for counting word occurrences.
- The 're' module for regular expression matching.

Functions:
1. get_top_terms_from_website(url)
    - url: The URL of the website to extract top terms from.
    - Returns: A list of the top 5 most common terms (words) in the website's text content.

The code sends a GET request to the specified URL, extracts text from the HTML content, tokenizes it, removes stopwords,
counts word occurrences, and identifies the top terms. The results are returned as a list of the top terms.

Note:
- Ensure that the required libraries are installed before using this script.
- The 'stopwords' list can be customized to include or exclude specific words that you want to filter out from the text.
"""

import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

# Define a list of common stopwords
stopwords = ["a", "an", "the", "me", "you", "we", "they", "it", "he", "she", "is", "am", "are", "was", "were", "his", "her", "your", "and", "also", "or", "not", "ours", "our", "their", "this", "that", "these", "mine", "in", "on", "at", "by", "for", "with", "about", "as", "if", "of", "from", "to", "up", "down", "under", "over", "between", "through", "after", "before", "while", "throughout", "since", "during", "until", "unless", "although", "because", "unless", "without", "throughout", "above", "below", "inside", "outside", "between", "among", "around", "before", "after", "along", "beside", "beneath", "across", "against", "toward", "besides", "into", "onto", "underneath", "upon", "within", "beyond", "inside", "outside", "near", "around"]

def get_top_terms_from_website(url):

    """
    Extract the top 5 terms from the text content of a website.

    :param url: The URL of the website to extract top terms from.

    :return: A list of the top 5 most common terms (words) in the website's text content.
    """

    print("--Code entered the get_top_terms_from_website function")
    print("|")

    try:
        # Send a GET request to the website
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text from the HTML content, excluding HTML tags
            text = soup.get_text()

            # Tokenize the extracted text by words and remove non-alphabetical characters
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
            print("--Code is about to exit the get_top_terms_from_website function\n")

            return top_terms

    except Exception as e:
        print(f"An error occurred: {str(e)}")

        print("|")
        print("--Code is about to exit the get_top_terms_from_website function\n")
        return []