import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import os

# Output file
csvFile = "phishTankDatabase.csv"

if not os.path.isfile(csvFile):
    with open(csvFile, "w", newline="") as outputFile:
        writer = csv.writer(outputFile)
        # Write the header of the CSV file
        writer.writerow(["URL"])

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

# Loop through all the pages
for page in range(0, 3):

    # Send a GET request to the webpage and get the HTML content
    # URL for confirmed Legitimate URLs
    # url = f"https://phishtank.org/phish_search.php?page={page}&valid=n&Search=Search"

    # URL for confirmed Phishing URLs
    url = f"https://phishtank.org/phish_search.php?page={page}&valid=y&Search=Search"

    driver.get(url)

    # EC is the Expected Condition, presence_of_element_located is the condition that the element is present on the page
    table_present = EC.presence_of_element_located((By.CLASS_NAME, "data"))
    # Wait for 10 seconds for the table to be present on the page
    WebDriverWait(driver, 10).until(table_present)

    # Parse the HTML content using BeautifulSoup, driver.page_source is the HTML content of the page
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the table that contains the data
    table = soup.find("table", {"class": "data"})

    # Get the rows in the table
    rows = table.find_all("tr")

    # Loop through each row in the table and extract the Phish ID and Phish URL
    for row in rows[1:]:
        cells = row.find_all("td")

        # Extract the Phish ID and Phish URL
        phish_id = cells[0].text.strip()

        # Send a GET request to the webpage and get the HTML content
        url = f"https://phishtank.org/phish_detail.php?phish_id={phish_id}"
        driver.get(url)

        # Parse the HTML content using BeautifulSoup, driver.page_source is the HTML content of the page
        newSoup = BeautifulSoup(driver.page_source, "html.parser")

        spanElement = newSoup.find('span', style='word-wrap:break-word;')

        if spanElement is not None:
            requiredURL = spanElement.find('b')

            if requiredURL is not None:
                url = requiredURL.text.strip()
                # If the URL is present then direct write it to the output file to avoid the exceptions of NoSuchElementException

                with open(csvFile, "a", newline="") as outputFile:
                    writer = csv.writer(outputFile)
                    writer.writerow([url]) 

                # print url to check if the code is working fine till this point or not, if not then at which URL is it failing
                print(url)
            
            else:
                print("<b> element not found.")
        else:
            print("<span> element not found.")        

        # Go back to the previous page
        driver.back()

# Close the Selenium driver
driver.quit()