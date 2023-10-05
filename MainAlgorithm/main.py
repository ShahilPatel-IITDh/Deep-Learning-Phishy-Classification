import os
import csv
from urllib.parse import urlsplit

# Import the screenshotCapture function from screenshotCapture.py which will be used to capture the full-page screenshot
from screenshotCapture import capture_full_page_screenshot

# Import the object_detection function from object_detection.py which will be used to detect the input box from the screenshot
from UI_Detection import detect_input_box
import logging

# Import the module to get the favicon of the website
from getLogo import scrape_favicon

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

if __name__ == "__main__":    
    
    # Open the CSV file containing the URLs
    with open(inputCSV_File, 'r') as file:

        reader = csv.reader(file)
        
        next(reader)  # Skip the header row
        
        for row in reader:
            
            counter += 1

            if counter == 10:
                break

            # Remove the whitespace from the URL
            url = row[1].strip()
            print(url)

            parsed_url = urlsplit(url)

            # Extract the domain name from the netloc component
            domain_name = parsed_url.netloc
            # Remove "www." if present at the beginning
            if domain_name.startswith("www."):
                domain_name = domain_name[4:]

            print("Domain name: ", domain_name)

            screenshotFile = os.path.join(screenShotDir, f"{domain_name}.png")

            # Capture the full-page screenshot
            capture_full_page_screenshot(url, screenshotFile)

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
            
            scrape_favicon(url, faviconDir, domain_name)

            logoFile = os.path.join(faviconDir, f"{domain_name}.ico")

            # Check if the logo file exists before running logo similarity detection
            if os.path.isfile(logoFile):
                
                # Run logo similarity detection code if the file exists

                # result = detect_logo_similarity(logoFile)

                if result == -1:
                    print("Logo similarity detected.")
                else:
                    print("Logo similarity not detected.")


            print(f"{counter}")
            print("----------------------------------\n")


    with open("contour-based-detection.txt", 'w') as file:
        file.write(f"Total number of URLs processed: {counter}\n")
        file.write(f"Total number of URLs with input boxes: {foundInputBox}\n")
        file.write(f"Total number of URLs without input boxes: {notFoundInputBox}\n")
    

    # with open("pytesseract-based-detection.txt", 'w') as file:
    #     file.write(f"Total number of URLs processed: {counter}\n")
    #     file.write(f"Total number of URLs with input boxes: {foundInputBox}\n")
    #     file.write(f"Total number of URLs without input boxes: {notFoundInputBox}\n")