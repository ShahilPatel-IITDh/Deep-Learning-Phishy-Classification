from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def google_search(domain, search_terms, reportFile):

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Enable headless mode
    chrome_options.add_argument('--disable-gpu')  # Disable GPU to prevent issues


    # Initialize ChromeDriver with ChromeDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chrome_options)
    
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

    time.sleep(20)

    # Extract the top 3 URLs
    top_urls = []
    for result in search_results[:3]:
        link = result.find_element(By.CSS_SELECTOR, "a")
        url = link.get_attribute("href")
        top_urls.append(url)

    # Close the Chrome WebDriver
    driver.quit()

    return top_urls