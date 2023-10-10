import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def get_top_terms_from_website(url):
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

            # Count the occurrences of each word
            word_counts = Counter(words)

            # Get the top 5 most common terms
            top_terms = word_counts.most_common(5)

            # Extract only the terms (ignore the counts)
            top_terms = [term for term, count in top_terms]

            return top_terms

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

# if __name__ == "__main__":
#     url = "https://example.com"  # Replace with the URL of the website you want to analyze
#     top_terms = get_top_terms_from_website(url)
#     print("Top 5 most occurring terms in the website's source code (excluding HTML tags):", top_terms)