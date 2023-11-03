import os
import csv
import time
from urllib.parse import urlsplit
import re

# Import the screenshotCapture function from screenshotCapture.py which will be used to capture the full-page screenshot
from screenshotCapture import capture_full_page_screenshot

# Import the object_detection function from object_detection.py which will be used to detect the input box from the screenshot
from UI_Detection import detect_input_box
import logging

# Import the extract_top_terms_from_screenshot function from frequentTerms_Checking.py which will be used to extract the top 5 most occurring terms from the screenshot
from frequentTerms_from_screenshot import extract_top_terms_from_screenshot

from frequentTerms_from_source_code import get_top_terms_from_website

# Import the search engine function from searchEngine.py which will be used to search the domain name and the top 5 most occurring terms on Google
from searchEngine import google_search

# Import the module to get the favicon of the website
from getLogo import scrape_favicon

# Check the logo similarity
from logoSimilarity import detect_logo_similarity

# Import the module which checks the difference between the input domain name and the domain name of the website
from domainName_Difference import check_Domain_similarity 

# inputCSV_File = os.path.join('..', 'URL_For_Testing', 'merged_URLs.csv')
screenShotDir = os.path.join('screenshots')
faviconDir = os.path.join('favicons-1000')

# report = os.path.join('..', 'report-for-100-Phishy-on-200-Logos')

report = os.path.join('..', 'report-for-testing-on-1000-Logos-test')

# Create the directory if it doesn't exist
if not os.path.exists(screenShotDir):
    os.makedirs(screenShotDir)

if not os.path.exists(faviconDir):
    os.makedirs(faviconDir)

if not os.path.exists(report):
    os.makedirs(report)

counter = 0

# Weighted Score
# 1. Input Box Detection: 33
# 2. Logo Similarity: 34
# 3. Domain Name dissimilarity from search engine and input domain : 33

def domainExtractor(url):
    # Define a regular expression pattern to match common URLs
    url_pattern = r'(https?://)?(www\d?\.)?(?P<domain>[\w-]+)\.(?P<tld>[\w.]+)'
    
    match = re.match(url_pattern, url)
    
    if match:
        domain = match.group('domain')
        return domain
    else:
        return url  # Return the original URL if the pattern doesn't match

def filter_valid_lists(lists):
    return [lst for lst in lists if lst is not None and len(lst) > 0]

def process_url(url, score):
    global counter

    start = time.time()
    print(f"URL to be processed is: {url}")

    # ---------------------------------------------------- Domain name extraction --------------------------------------------- #
    # Extract the domain name from the netloc component
    input_domain_name = domainExtractor(url)

    print("Input Domain Name: ", input_domain_name)
            
    # Final report file for the URL
    reportFile = os.path.join(report, f"{input_domain_name}.txt")

    # ---------------------------------------------------- Screen Shot Capturing ---------------------------------------------------- # 

    screenshotFile = os.path.join(screenShotDir, f"{input_domain_name}.png")
    # print("The name of Screenshot file will be: ", screenshotFile)

    # Capture the full-page screenshot
    capture_full_page_screenshot(url, screenshotFile)

    # ---------------------------------------------------- UI detection ---------------------------------------------------- # 

    # Check if the output file exists before running UI detection
    if os.path.isfile(screenshotFile):
                
        # Run UI detection code if the file exists
        result = detect_input_box(screenshotFile)

        if result == -1:
            score += -18
            with open (reportFile, 'w') as file:
                file.write(f"Input box detected in screenshot: {score}\n")

        else:
            score += 18
            with open (reportFile, 'w') as file:
                file.write(f"Input box not detected in screenshot: {score}\n")
            
    else:
        score += -18
        with open (reportFile, 'w') as file:
            file.write(f"screenshot doesn't exist: {score}\n")

            
    # ---------------------------------------------------- Frequent terms extraction ------------------------------------------- #
            
    # ----------------------------------------  From Screenshot ------------------------------------------ #

    # Check if the output file exists before running frequent terms extraction
    if os.path.isfile(screenshotFile):
                    
        # Run frequent terms extraction code if the file exists
        top_terms_from_screenshot = extract_top_terms_from_screenshot(input_domain_name, screenshotFile)

        with open(reportFile, 'a') as file:
            file.write(f"Top 5 most occurring terms from screenshot: {top_terms_from_screenshot}\n")
            
    else:
        top_terms_from_screenshot = [] #Initialize it as an empty list.
        with open(reportFile, 'a') as file:
            file.write(f"Screenshot doesn't exist for so frequent terms not found: {input_domain_name}\n")

            
    # -----------------------------------------  From Source Code ------------------------------------------ #

    top_terms_from_source_code = get_top_terms_from_website(url)

    if top_terms_from_source_code is None:
        with open (reportFile, 'a') as file:
            file.write("No terms found, website not working!!\n")
            
    else:
        with open (reportFile, 'a') as file:
            file.write(f"Top 5 most occurring terms in the website's source code: {top_terms_from_source_code}\n")

            
    # Final list of the top most occurring terms
    # Function to remove None and empty lists

    # Filter and combine valid lists
    valid_lists = filter_valid_lists([top_terms_from_screenshot, top_terms_from_source_code])

    # valid_lists = filter_valid_lists([top_terms_from_source_code])

    if valid_lists:
        # Concatenate and create a set to remove duplicates
        unique_terms_set = set(item for sublist in valid_lists for item in sublist)

        # Convert the set back to a list
        top_terms = list(unique_terms_set)

    else:
        top_terms = []

        with open (reportFile, 'a') as file:
            file.write(f"final list of most occurring terms is: {top_terms}\n")


    # ------------------------------- Searching domain + frequent terms on search engine --------------------------------------- #

    topDomains = google_search(input_domain_name, top_terms, reportFile)

    # print(f"Top URLs for {input_domain_name}:", topURLs)   

    unique_domains = set()

    for domain in topDomains:
        domain = domainExtractor(domain)

        # Add the domain name to the set
        unique_domains.add(domain)
            
    with open(reportFile, 'a') as file:
        file.write(f"Unique domains: {unique_domains}\n")

    if unique_domains is None:
        score += -65

        with open(reportFile, 'a') as file:
            file.write(f"Unique domains not found.: {score}\n")

    else:
        # Checking if the input_domain as string is present in any string of the unique_domains list
        stringFound = False

        # Iterate over the unique_domains set
        for domain in unique_domains:
            if input_domain_name in domain:
                stringFound = True
                break  # Exit the loop early if a match is found

        if stringFound:
            # Do something if the input domain is found in the set
            score += 65
            with open(reportFile, 'a') as file:
                file.write(f"{input_domain_name} is in the list of unique domains (+65): {score}\n")
                    
        else:
            score += -65
            with open(reportFile, 'a') as file:
                file.write(f"{input_domain_name} is not in the list of unique domains (-65): {score}\n")

            
    # ---------------------------------------------------- Favicon scraping ---------------------------------------------------- #
            
    logoFile = os.path.join(faviconDir, f"{input_domain_name}")

    # print(f"logoFile will be {logoFile}")

    scrape_favicon(url, logoFile, input_domain_name)

    extensions = ['.ico', '.png', '.jpeg', '.jpg', '.svg']

    logoDatabase = os.path.join('..', 'Top_Logos_1000')

    # ------------------------------------------------ Logo similarity detection ------------------------------------------ #

    time.sleep(2)
    print(f"Logo file: {logoFile}")

    # Check if the logo file exists before running logo similarity detection

    allScoresList = []
    for ext in extensions:

        if os.path.isfile(logoFile+ext):
            # print(f"Testing for {logoFile+ext}")
                    
            # Run logo similarity detection code if the file exists
            similarLogos = detect_logo_similarity(input_domain_name, logoFile+ext, logoDatabase, reportFile)

            if not similarLogos:  # Check if the dictionary is empty
                print("Logo similarity not detected.")
                # There may be a case where the a logo is not found in the database but the site is legitimate, so we will add a positive score
                score += 0
                allScoresList.append(score)
                with open (reportFile, 'a') as file:
                    file.write(f"Logo similarity not detected (+0): {score}\n")
                
                break

            else:
                # As the similarity is detected, we will now check if the domains are same or not, if not then it will add negative score, else positive score
                print("Logo similarity detected:")
                for logo, mse in similarLogos.items():                            
                    # Check the difference in the input domain name and the logo name (limited to 3 decimal places)

                    logoDomain = logo[:-4]
                    domainSimilarity = round(check_Domain_similarity(input_domain_name, logoDomain), 3)

                    if domainSimilarity < 0.70:
                        score += -17
                        allScoresList.append(score)
                            
                    else:
                        score += 17
                        allScoresList.append(score)

                    with open(reportFile, 'a') as file:
                        file.write(f"Domain Similarity with {logo}: {domainSimilarity}%; score =  {score}\n")
                    
            # break

        # Most of the phishing websites don't have any logos, so we will add a negative score if the logo is not found
        else:
            score+= -17
            allScoresList.append(score)
            with open (reportFile, 'a') as file:
                file.write(f"Logo not found (-17): {score}\n")

    with open(reportFile, 'a') as file:
        file.write(f"allScoresList is: {allScoresList}\n")
        
    score = max(allScoresList)
            
    # ------------------------------------------------ End of the Algorithm ------------------------------------------ #

    end = time.time()

    timeTaken = end - start

    # The final score can vary from -100 to 100
            
    with open(reportFile, 'a') as file:
        file.write(f"The weighted score is {score}")

        if score <= 45:
            file.write(f" and the website is Phishy\n")
                
        elif score > 45 and score < 64:
            file.write(f" and the website is Suspicious\n")
                
        else:
            file.write(f" and the website is Legitimate\n")

        file.write(f"Time taken to process the URL: {timeTaken:.2f} seconds\n")
        file.write(f"----------------------------------\n")

    #------------------------------------------------- Counters for code checking ----------------------------------------------#

    print(f"{counter}")
    print("----------------------------------\n")

if __name__ == "__main__":    
    
    print("Code started\n")

    # Ask the user for input type
    input_type = input("Enter 'S' for a single URL or 'C' for a CSV file: ").strip().lower()
    
    if input_type == 's':
        # Process a single URL
        url = input("Enter the URL: ").strip()
        process_url(url, 0)
    
    elif input_type == 'c':
        # Process URLs from a CSV file
        csv_file_path = input("Enter the path of the CSV file: ").strip()
        
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            
            for row in reader:
                url = row[0].strip()
                process_url(url, 0)
    else:
        print("Invalid input type. Please enter 'S' for a single URL or 'C' for a CSV file.")