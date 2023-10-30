"""
Google Search and Result Extraction Documentation

This Python code is designed to perform a Google search using a specified domain and search terms. It automates the process
of entering the search query in Google, retrieving search results, extracting top URLs, and closing the web browser. Additionally,
it can capture full-page screenshots of the search results. The code is primarily built using the Selenium library.

Usage:
To use this script, call the 'google_search' function with the following parameters:
- domain: The domain to be used in the search query.
- search_terms: A list of search terms to be added to the query.
- reportFile: The file to which search-related information is logged.

Example:
top_domains = google_search("example.com", ["example", "website", "search"], "search_report.txt")

Dependencies:
- Python 3.x
- The 'urllib.parse' module for parsing URLs.
- The 'selenium' library for automating web browser actions.
- The 'webdriver_manager.chrome' module for managing the Chrome WebDriver.
- The 'screenshotCapture' module (imported but not used) for capturing full-page screenshots.
- The 'os' module for managing directories and files.
- The 'fake_useragent' library for generating random user agents.
- The 'time' module for managing timing and delays.

Functions:
1. google_search(domain, search_terms, reportFile)
    - domain: The domain to be used in the search query.
    - search_terms: A list of search terms to be added to the query.
    - reportFile: The file to which search-related information is logged.
    - Returns: A list of the top domains from the search results.

The code sets up a Chrome web driver with specific options, enters a search query into Google, retrieves search results,
extracts top domains from the results, and closes the web browser.

Note:
- Ensure that the required libraries are installed before using this script.
- Some parts of the code (e.g., taking screenshots) are commented out but can be enabled if needed.
"""

from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
# import chromedriver_autoinstaller
import os
from fake_useragent import UserAgent

# Import the screenshotCapture function from screenshotCapture.py which will be used to capture the full-page screenshot
from screenshotCapture import capture_full_page_screenshot

def google_search(domain, search_terms, reportFile):

    """
    Perform a Google search with the specified domain and search terms and extract the top domains from the results.

    :param domain: The domain to be used in the search query.
    :param search_terms: A list of search terms to be added to the query.
    :param reportFile: The file to which search-related information is logged.

    :return: A list of the top domains from the search results.
    """

    print("--Code entered the google_search function")
    print("|")

    # chrome_options = webdriver.ChromeOptions()
    
    chrome_options = Options()
    # Run Chrome in headless mode
    # chrome_options.add_argument("--headless")
    # Disable the GPU 
    chrome_options.add_argument("--disable-gpu")
    # Disable the sandbox
    chrome_options.add_argument("--no-sandbox")
    # Disable the DevShmUsage
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize ChromeDriver with ChromeDriverManager
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # chromedriver_autoinstaller.install()

    # driver = webdriver.Chrome(options=chrome_options)

    # Create a UserAgent object to generate a random user agent
    ua = UserAgent()
    user_agent = ua.random
    with open(reportFile, 'a') as file:
        file.write(f"user agent = f{user_agent}")
    
    # Set the user agent in the ChromeOptions
    # chrome_options.add_argument(f"user-agent={user_agent}")
    
    chrome_options.add_argument(f"user-agent = Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
    
    # Initialize the web driver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    
    search_string = " ".join(search_terms)

    # Combine domain and search terms to form the search query
    search_query = f'{domain} ' + (search_string)

    with open(reportFile, 'a') as file:
        file.write(f"search query will be {search_query}\n")

    # Open google.com in Chrome
    driver.get("https://www.google.com")

    # Find the search input element and enter the search query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # Wait for the search results to load (you may need to adjust the time)
    driver.implicitly_wait(5)

    # Find the search result elements (links)
    search_results = driver.find_elements(By.CSS_SELECTOR, ".tF2Cxc")

    # Extract the top 3 URLs
    top_domains = []
    top_urls = []

    for result in search_results[:3]:
        link = result.find_element(By.CSS_SELECTOR, "a")
        url = link.get_attribute("href")
        top_urls.append(url)

        # Parse the URL
        parsed_url = urlparse(url)

        # Extract the domain
        domain = parsed_url.netloc

        top_domains.append(domain)

    # Close the Chrome WebDriver
    driver.quit()

    print("|")
    print("--Code is about to exit the google_search function\n")

    return top_domains