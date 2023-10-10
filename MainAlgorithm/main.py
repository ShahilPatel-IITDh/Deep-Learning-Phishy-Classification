import os
import csv
from urllib.parse import urlsplit

# Import the screenshotCapture function from screenshotCapture.py which will be used to capture the full-page screenshot
from screenshotCapture import capture_full_page_screenshot

# Import the object_detection function from object_detection.py which will be used to detect the input box from the screenshot
from UI_Detection import detect_input_box
import logging

# Import the extract_top_terms_from_screenshot function from frequentTerms_Checking.py which will be used to extract the top 5 most occurring terms from the screenshot
from frequentTerms_from_screenshot import extract_top_terms_from_screenshot

from frequentTerms_from_source_code import get_top_terms_from_website

# Import the module to get the favicon of the website
# from getLogo import scrape_favicon

# Check the logo similarity
# from logoSimilarity import detect_logo_similarity

inputCSV_File = os.path.join('..', 'URL_For_Testing', 'phishTankDatabase.csv')
screenShotDir = os.path.join('screenshots')
faviconDir = os.path.join('favicons')


# Create the directory if it doesn't exist
if not os.path.exists(screenShotDir):
    os.makedirs(screenShotDir)

if not os.path.exists(faviconDir):
    os.makedirs(faviconDir)

counter = 0
foundInputBox = 0
notFoundInputBox = 0
screenshotNotPresent = 0
faviconsFound = 0
faviconsNotFound = 0

def filter_valid_lists(lists):
    return [lst for lst in lists if lst is not None and len(lst) > 0]


if __name__ == "__main__":    
    
    print("Code started\n")

    # Open the CSV file containing the URLs
    with open(inputCSV_File, 'r') as file:

        reader = csv.reader(file)
        
        next(reader)  # Skip the header row
        
        for row in reader:
            
            counter += 1

            # if counter == 2:
            #     break

            # Remove the whitespace from the URL
            url = row[1].strip()

            # url = "https://www.fdd.org/analysis/2023/10/08/attacks-on-israel-part-of-irans-ring-of-fire-strategy/"

            print(url)

            # ---------------------------------------------------- Domain name extraction ---------------------------------------------------- #

            parsed_url = urlsplit(url)

            # Extract the domain name from the netloc component
            domain_name = parsed_url.netloc

            # Remove "www." if present at the beginning
            if domain_name.startswith("www."):
                domain_name = domain_name[4:]
            
            if domain_name.startswith("http.www."):
                domain_name = domain_name[10:]
            
            if domain_name.startswith("https."):
                domain_name = domain_name[6:]

            print("Domain name: ", domain_name)

            # ---------------------------------------------------- Screen Shot Capturing ---------------------------------------------------- # 

            screenshotFile = os.path.join(screenShotDir, f"{domain_name}.png")
            print("The name of Screenshot file will be: ", screenshotFile)

            # Capture the full-page screenshot
            capture_full_page_screenshot(url, screenshotFile)

            # ---------------------------------------------------- UI detection ---------------------------------------------------- # 

            # Check if the output file exists before running UI detection
            if os.path.isfile(screenshotFile):
                
                # Run UI detection code if the file exists
                result = detect_input_box(screenshotFile)

                if result == -1:
                    foundInputBox += 1
                    print("Input box detected.")

                else:
                    notFoundInputBox += 1
                    print("Input box not detected.")
            
            else:
                print(f"Screenshot doesn't exist for: {domain_name}")
                screenshotNotPresent += 1

            
            # ---------------------------------------------------- Frequent terms extraction ------------------------------------------- #
            
            # From Screenshot
            # Check if the output file exists before running frequent terms extraction
            if os.path.isfile(screenshotFile):
                    
                    # Run frequent terms extraction code if the file exists
                    top_terms_from_screenshot = extract_top_terms_from_screenshot(domain_name, screenshotFile)
    
                    print(f"Top 5 most occurring terms for {domain_name}:", top_terms_from_screenshot)
            
            else:
                print(f"Screenshot doesn't exist for so frequent terms not found: {domain_name}")
            
            # From Source Code

            top_terms_from_source_code = get_top_terms_from_website(url)

            if top_terms_from_source_code is None:
                print("No terms found, website not working")
            
            else:
                print("Top 5 most occurring terms in the website's source code:", top_terms_from_source_code)

            
            # Final list of the top most occurring terms
            # Function to remove None and empty lists

            # Filter and combine valid lists
            valid_lists = filter_valid_lists([top_terms_from_screenshot, top_terms_from_source_code])

            if valid_lists:
                # Concatenate and create a set to remove duplicates
                unique_terms_set = set(item for sublist in valid_lists for item in sublist)
                # Convert the set back to a list
                top_terms = list(unique_terms_set)

            else:
                top_terms = []

            print(f"final list of most occurring terms is: {top_terms}")
            
            # ---------------------------------------------------- Favicon scraping ---------------------------------------------------- #
            
            # logoFile = os.path.join(faviconDir, f"{domain_name}.ico")

            # scrape_favicon(url, logoFile, domain_name)

            # if os.path.isfile(logoFile):
            #     faviconsFound += 1
            #     print("Logo found")
            
            # else:
            #     faviconsNotFound += 1
            #     print("Logo NOT found")


            # logoDatabase = os.path.join('..', 'SampleLogos')

            # ------------------------------------------------ Logo similarity detection ------------------------------------------ #

            # Check if the logo file exists before running logo similarity detection
            # if os.path.isfile(logoFile):
                
            #     # Run logo similarity detection code if the file exists

            #     similarLogos = detect_logo_similarity(logoFile, logoDatabase)

            #     if not similarLogos:  # Check if the dictionary is empty
            #         print("Logo similarity not detected.")

            #     else:
            #         print("Logo similarity detected:")
            #         for logo, similarity in similarLogos.items():
            #             with open(f"{domain_name}.txt", 'a') as file:
            #                 file.write(f"Logo: {logo}, Similarity Score: {similarity:.2f}%\n")

            # else:
            #     print(f"Logo doesn't exist for: {domain_name}")


            #--------------------------------------------------------- Counters for code checking ------------------------------------------------#

            print(f"{counter}")
            print("----------------------------------\n")


    # with open("contour-based-detection.txt", 'w') as file:
    #     file.write(f"Total number of URLs processed: {counter}\n")
    #     file.write(f"Total number of URLs with input boxes: {foundInputBox}\n")
    #     file.write(f"Total number of URLs without input boxes: {notFoundInputBox}\n")
    #     file.write(f"Total number of URLs without screenshots: {screenshotNotPresent}\n")
    

    # with open("pytesseract-based-detection.txt", 'w') as file:
    #     file.write(f"Total number of URLs processed: {counter}\n")
    #     file.write(f"Total number of URLs with input boxes: {foundInputBox}\n")
    #     file.write(f"Total number of URLs without input boxes: {notFoundInputBox}\n")
    #     file.write(f"Total number of URLs without screenshots: {screenshotNotPresent}\n")
    
    # with open('favicons-stat.txt', 'w') as file:
    #     file.write(f"Total number of URLs processed: {counter}\n")
    #     file.write(f"Total number of URLs with favicons: {faviconsFound}\n")
    #     file.write(f"Total number of URLs without favicons: {faviconsNotFound}\n")