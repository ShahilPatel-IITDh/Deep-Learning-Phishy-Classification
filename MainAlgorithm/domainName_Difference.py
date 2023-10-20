import Levenshtein

def check_Domain_similarity(inputDomain, similarDomain):
    print("Code entered the check_Domain_similarity function")

    distance = Levenshtein.distance(inputDomain, similarDomain)

    # Calculate similarity as a ratio of the distance and the length of the longer string
    max_len = max(len(inputDomain), len(similarDomain))
    similarity = (max_len - distance) / max_len

    print("Code is about to exit the check_Domain_similarity function")

    return similarity*100