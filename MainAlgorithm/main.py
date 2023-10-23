import os
import csv
import time
from urllib.parse import urlsplit

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

inputCSV_File = os.path.join('..', 'URL_For_Testing', 'merged_URLs.csv')
screenShotDir = os.path.join('screenshots-10')
faviconDir = os.path.join('favicons-10')

# report = os.path.join('..', 'report-for-100-Phishy-on-200-Logos')

report = os.path.join('..', 'report-for-testing-10-Logos')

# Create the directory if it doesn't exist
if not os.path.exists(screenShotDir):
    os.makedirs(screenShotDir)

if not os.path.exists(faviconDir):
    os.makedirs(faviconDir)

if not os.path.exists(report):
    os.makedirs(report)

counter = 0
foundInputBox = 0
notFoundInputBox = 0
screenshotNotPresent = 0
faviconsFound = 0
faviconsNotFound = 0

# Weighted Score
# 1. Input Box Detection: 33
# 2. Logo Similarity: 34
# 3. Domain Name dissimilarity from search engine and input domain : 33

score = 0

def filter_valid_lists(lists):
    return [lst for lst in lists if lst is not None and len(lst) > 0]

if __name__ == "__main__":    
    
    print("Code started\n")

    # Open the CSV file containing the URLs
    with open(inputCSV_File, 'r') as file:

        reader = csv.reader(file)
        
        next(reader)  # Skip the header row
        
        for row in reader:

            # get time taken to process each URL (end-to-end)

            start = time.time()
            
            counter += 1

            if counter == 2:
                break

            # Remove the whitespace from the URL
            url = row[0].strip()

            url = "https://www.roku.com/intl?next=/&source=www.roku.com"

            print(url)

            # ---------------------------------------------------- Domain name extraction --------------------------------------------- #

            parsed_url = urlsplit(url)

            # Extract the domain name from the netloc component
            input_domain_name = parsed_url.netloc

            # Remove "www." if present at the beginning
            if input_domain_name.startswith("www."):
                input_domain_name = input_domain_name[4:]
            
            if input_domain_name.startswith("http.www."):
                input_domain_name = input_domain_name[10:]
            
            if input_domain_name.startswith("https."):
                input_domain_name = input_domain_name[6:]

            print("Input Domain Name: ", input_domain_name)
            
            # Final report file for the URL
            reportFile = os.path.join(report, f"{input_domain_name}.txt")

            # ---------------------------------------------------- Screen Shot Capturing ---------------------------------------------------- # 

            screenshotFile = os.path.join(screenShotDir, f"{input_domain_name}.png")
            print("The name of Screenshot file will be: ", screenshotFile)

            # Capture the full-page screenshot
            capture_full_page_screenshot(url, screenshotFile)

            # ---------------------------------------------------- UI detection ---------------------------------------------------- # 

            # Check if the output file exists before running UI detection
            if os.path.isfile(screenshotFile):
                
                # Run UI detection code if the file exists
                result = detect_input_box(screenshotFile)

                if result == -1:
                    score += -33
                    foundInputBox += 1
                    with open (reportFile, 'w') as file:
                        file.write(f"Input box detected in screenshot\n")

                else:
                    score += 33
                    notFoundInputBox += 1
                    with open (reportFile, 'w') as file:
                        file.write(f"Input box not detected in screenshot\n")
            
            else:
                score += 0
                screenshotNotPresent += 1
                with open (reportFile, 'w') as file:
                    file.write(f"screenshot doesn't exist.\n")

            
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
                # parsed_url = urlsplit(url)

                # # Extract the domain name from the netloc component
                # domain_name = parsed_url.netloc

                # Remove "www." if present at the beginning
                if domain.startswith("www."):
                    domain = domain[4:]
                
                if domain.startswith("http.www."):
                    domain = domain[10:]
                
                if domain.startswith("https."):
                    domain = domain[6:]
                
                # Add the domain name to the set
                print(f"after-processing-{domain}")
                unique_domains.add(domain)
            
            with open(reportFile, 'a') as file:
                file.write(f"Unique domains: {unique_domains}\n")

            if unique_domains is None:
                score += 0

            # Check if the input_domain_name is in the list of domains obtained from the search engine
            # if input_domain_name in unique_domains:
            #     score += 33
            #     with open(reportFile, 'a') as file:
            #         file.write(f"{input_domain_name} is in the list of unique domains.\n")

            # else:
            #     score += -33
            #     with open(reportFile, 'a') as file:
            #         file.write(f"{input_domain_name} is not in the list of unique domains.\n")

            # Checking if the input_domain as string is present in any string of the unique_domains list
            stringFound = False

            # Iterate over the unique_domains set
            for domain in unique_domains:
                if input_domain_name in domain:
                    stringFound = True
                    break  # Exit the loop early if a match is found

            if stringFound:
                # Do something if the input domain is found in the set
                score += 33
                with open(reportFile, 'a') as file:
                    file.write(f"{input_domain_name} is in the list of unique domains.\n")
                
            else:
                score += -33
                with open(reportFile, 'a') as file:
                    file.write(f"{input_domain_name} is not in the list of unique domains.\n")

            
            # ---------------------------------------------------- Favicon scraping ---------------------------------------------------- #
            
            logoFile = os.path.join(faviconDir, f"{input_domain_name}")

            # print(f"logoFile will be {logoFile}")

            scrape_favicon(url, logoFile, input_domain_name)

            extensions = ['.ico', '.png', '.jpeg', '.jpg', '.svg']

            for ext in extensions:
                if os.path.isfile(logoFile+ext):
                    faviconsFound += 1
                    with open(reportFile, 'a') as file:
                        file.write(f"Favicon found\n")
                    break
                
                else:
                    faviconsNotFound += 1
                    with open(reportFile, 'a') as file:
                        file.write(f"Favicon not found\n")

            logoDatabase = os.path.join('..', 'Logos-10')

            # ------------------------------------------------ Logo similarity detection ------------------------------------------ #

            time.sleep(2)
            print(f"Logo file: {logoFile}")

            # Check if the logo file exists before running logo similarity detection
            for ext in extensions:

                if os.path.isfile(logoFile+ext):

                    print(f"Testing for {logoFile+ext}")
                    
                    # Run logo similarity detection code if the file exists
                    similarLogos = detect_logo_similarity(input_domain_name, logoFile+ext, logoDatabase, reportFile)

                    if not similarLogos:  # Check if the dictionary is empty
                        print("Logo similarity not detected.")
                        score += 0
                        with open (reportFile, 'a') as file:
                            file.write(f"Logo similarity not detected.\n")

                    else:

                        # As the similarity is detected, we will now check if the domains are same or not, if not then it will add negative score, else positive score
                        print("Logo similarity detected:")
                        for logo, mse in similarLogos.items():                            
                            # Check the difference in the input domain name and the logo name (limited to 3 decimal places)
                            domainSimilarity = round(check_Domain_similarity(input_domain_name, logo), 3)

                            if domainSimilarity < 0.60:
                                score += -34
                            
                            else:
                                score += 34

                            with open(reportFile, 'a') as file:
                                file.write(f"Domain Similarity with {logo}: {domainSimilarity}%\n")
                else:
                    score+=0

            end = time.time()

            timeTaken = end - start

            # The final score can vary from -100 to 100
            
            with open(reportFile, 'a') as file:
                file.write(f"The weighted score is {score}")

                if score < 33:
                    file.write(f" and the website is Phishy\n")
                
                elif score >= 33 and score <= 66:
                    file.write(f" and the website is Suspicious\n")
                
                elif score>66:
                    file.write(f" and the website is Legitimate\n")

                file.write(f"Time taken to process the URL: {timeTaken:.2f} seconds\n")
                file.write(f"----------------------------------\n")

            #------------------------------------------------- Counters for code checking ----------------------------------------------#

            print(f"{counter}")
            print("----------------------------------\n")