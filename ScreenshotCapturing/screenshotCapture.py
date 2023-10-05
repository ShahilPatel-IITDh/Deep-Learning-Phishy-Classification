import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

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

outputDir = os.path.join('..', 'URL_For_Testing', 'screenshots')

# Create the directory if it doesn't exist
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

# Open the CSV file containing the URLs
with open(inputCSV_File, 'r') as file:

    reader = csv.reader(file)
    
    next(reader)  # Skip the header row
    
    for row in reader:
        
        # Remove the whitespace from the URL
        url = row[1].strip()
        print(url)

        driver.get(url)
        
        # Set the path of the screenshot file
        screenshot_file_path = os.path.join(outputDir, f'{url}.png')

        # Take a screenshot of the landing page
        driver.save_screenshot(screenshot_file_path)
        
    
    driver.quit()
