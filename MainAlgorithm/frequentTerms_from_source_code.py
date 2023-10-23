import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

# Define a list of common stopwords
stopwords = ["a", "an", "the", "me", "you", "we", "they", "it", "he", "she", "is", "am", "are", "was", "were", "his", "her", "your", "and", "also", "or", "not", "ours", "our", "their", "this", "that", "these", "mine", "in", "on", "at", "by", "for", "with", "about", "as", "if", "of", "from", "to", "up", "down", "under", "over", "between", "through", "after", "before", "while", "throughout", "since", "during", "until", "unless", "although", "because", "unless", "without", "throughout", "above", "below", "inside", "outside", "between", "among", "around", "before", "after", "along", "beside", "beneath", "across", "against", "toward", "besides", "into", "onto", "underneath", "upon", "within", "beyond", "inside", "outside", "near", "around"]

def get_top_terms_from_website(url):

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