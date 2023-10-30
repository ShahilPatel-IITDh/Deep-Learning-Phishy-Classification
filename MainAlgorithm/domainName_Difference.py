"""
Domain Similarity Checker Documentation

This Python code defines a function to check the similarity between two domain names using the Levenshtein distance algorithm.
The Levenshtein distance is a measure of the difference between two strings by calculating the minimum number of single-character
edits (insertions, deletions, or substitutions) required to transform one string into the other.

Usage:
To use this script, call the 'check_Domain_similarity' function with the following parameters:
- inputDomain: The first domain name to be compared.
- similarDomain: The second domain name to be compared.

Example:
check_Domain_similarity("example.com", "example.net")

Dependencies:
- Python 3.x
- The 'Levenshtein' library for Levenshtein distance calculation.

Functions:
1. check_Domain_similarity(inputDomain, similarDomain)
    - inputDomain: The first domain name for comparison.
    - similarDomain: The second domain name for comparison.
    - Returns: A similarity score as a percentage based on the Levenshtein distance. A higher score indicates greater similarity.

The code calculates the Levenshtein distance between the two domain names and converts it into a similarity score. The result is a
percentage, with 100% indicating that the two domain names are identical and 0% indicating no similarity.

Note:
- Ensure that the 'Levenshtein' library is installed before using this script.
"""

import Levenshtein

def check_Domain_similarity(inputDomain, similarDomain):
    
    """
    Check the similarity between two domain names using the Levenshtein distance algorithm.

    :param inputDomain: The first domain name for comparison.
    :param similarDomain: The second domain name for comparison.

    :return: A similarity score as a percentage based on the Levenshtein distance.
    """

    print("--Code entered the check_Domain_similarity function")
    print("|")

    distance = Levenshtein.distance(inputDomain, similarDomain)

    # Calculate similarity as a ratio of the distance and the length of the longer string
    max_len = max(len(inputDomain), len(similarDomain))
    similarity = (max_len - distance) / max_len

    print("|")
    print("--Code is about to exit the check_Domain_similarity function\n")

    return similarity*100