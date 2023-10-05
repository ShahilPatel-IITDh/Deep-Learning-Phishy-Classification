import os
import csv
import time
import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlsplit
from PIL import Image
import io

# Import the object_detection function from object_detection.py which will be used to detect the input box from the screenshot
from UI_Detection import detect_input_box
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Set up Chrome options
chrome_options = Options()
# Run Chrome in headless mode
chrome_options.add_argument("--headless") 
# Disable the GPU 
chrome_options.add_argument("--disable-gpu")
# Disable the sandbox
chrome_options.add_argument("--no-sandbox")
# Disable the DevShmUsage
chrome_options.add_argument("--disable-dev-shm-usage")

# Install and Initialize WebDriver using webdriver_manager (This will not require to pre-download the chrome driver)
driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()

inputCSV_File = os.path.join('..', 'URL_For_Testing', 'phishTankDatabase.csv')

outputDir = os.path.join('screenshots')

# Create the directory if it doesn't exist
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

counter = 0


def capture_full_page_screenshot(url, output_file):
    try:
        driver.get(url)

        # Handle WebDriverException (e.g., net::ERR_NAME_NOT_RESOLVED)
        if "ERR_NAME_NOT_RESOLVED" in driver.page_source:
            print(f"Error: {url} could not be resolved. Skipping...")
            return

        # Get the page height
        page_height = driver.execute_script("return document.body.scrollHeight")

        # Set the initial viewport height
        viewport_height = driver.execute_script("return window.innerHeight")

        # Calculate the number of viewport captures needed
        num_captures = (page_height + viewport_height - 1) // viewport_height

        # Capture and stitch the screenshots
        screenshots = []

        for i in range(num_captures):
            screenshot = driver.get_screenshot_as_png()
            screenshots.append(Image.open(io.BytesIO(screenshot)))
            driver.execute_script(f"window.scrollTo(0, {viewport_height * (i + 1)});")

            time.sleep(2)

        # Stitch the screenshots vertically
        full_page_screenshot = Image.new("RGB", (screenshots[0].width, page_height))
        y_offset = 0

        for screenshot in screenshots:
            full_page_screenshot.paste(screenshot, (0, y_offset))
            y_offset += screenshot.height

        # Save the full-page screenshot
        full_page_screenshot.save(output_file)

    except WebDriverException as e:
        # Log the WebDriverException
        logging.error(f"WebDriverException while processing URL: {url}. Error: {str(e)}")
    except Exception as e:
        # Log other exceptions
        logging.error(f"WebDriverException while processing URL: {url}. Error: {str(e)}")

foundInputBox = 0
notFoundInputBox = 0

if __name__ == "__main__":    
    
    # Open the CSV file containing the URLs
    with open(inputCSV_File, 'r') as file:

        reader = csv.reader(file)
        
        next(reader)  # Skip the header row
        
        for row in reader:
            
            counter += 1

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

            outputFile = os.path.join(outputDir, f"{domain_name}.png")

            # Capture the full-page screenshot
            capture_full_page_screenshot(url, outputFile)

            # Check if the output file exists before running UI detection
            if os.path.isfile(outputFile):
                
                # Run UI detection code if the file exists
                result = detect_input_box(outputFile)

                if result == -1:
                    foundInputBox += 1
                    print("Input box detected.")

                else:
                    notFoundInputBox += 1
                    print("Input box not detected.")


            print(f"{counter}")
            print("----------------------------------\n")


        driver.quit()
        
    with open("contour-based-detection.txt", 'w') as file:
        file.write("Total number of URLs processed: ", counter)
        file.write("Total number of URLs with input boxes: ", foundInputBox)
        file.write("Total number of URLs without input boxes: ", notFoundInputBox)
