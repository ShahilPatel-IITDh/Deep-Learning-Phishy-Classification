import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Selenium imports
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import WebDriverException, TimeoutException, InvalidSessionIdException, NoSuchElementException


# Specify the desired Chrome WebDriver version
# chrome_version = '117.0.5938'

# # Use ChromeDriverManager to automatically download and manage the Chrome WebDriver executable
# webdriver_path = ChromeDriverManager(driver_version=chrome_version).install()

# # Create Chrome options
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--incognito')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument("--proxy-server=http://your-proxy-server:port")

# # Create a Chrome WebDriver instance with the specified options
# driver = webdriver.Chrome(
#     options=chrome_options
# )



headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}


# Create the Logos directory if it doesn't exist in the Logo_fetching directory
logos_dir = os.path.join('..', 'Logos')
screenshots_dir = os.path.join('..', 'Screenshots')
outputs = os.path.join('..', 'outputs')


# Make the directory to store Logos if it doesn't exist
if not os.path.exists(logos_dir):
    os.mkdir(logos_dir)
    
# Make the directory to store Screenshots if it doesn't exist
if not os.path.exists(screenshots_dir):
    os.mkdir(screenshots_dir)
    
# Make the directory to store outputs if it doesn't exist
if not os.path.exists(outputs):
    os.mkdir(outputs)

Exceptions = os.path.join(outputs, 'Exceptions.txt')

def scrape_Favicon(URL, Favicons_Directory, domain):

    try:
        # Fetch the web page content
        response = requests.get(URL, headers=headers, timeout=5)
        
        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Failed to fetch {URL}, status code: {response.status_code}")

        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        #  List of favicon link types to check
        favicon_link_types = ['icon', 'apple-touch-icon', 'shortcut icon', 'mask-icon', 'fluid-icon', 'manifest', 'yandex-tableau-widget', 'apple-touch-startup-image', 'apple-touch-icon-precomposed']

        # Find the favicon URL
        favicon_URL = None

        for link_type in favicon_link_types:
            link_tags = soup.find_all('link', rel=link_type)

            for link_tag in link_tags:
                if 'href' in link_tag.attrs:
                    favicon_URL = urljoin(URL, link_tag['href'])
                    break

            if favicon_URL:
                break

            # If a favicon URL is found, download the favicon

        if favicon_URL:
            favicon_response = requests.get(favicon_URL)

            if favicon_response.status_code == 200:

                favicon_content = favicon_response.content

                # Remove any extension from the domain name
                filename, _ = os.path.splitext(domain)

                with open(os.path.join(Favicons_Directory, filename+'.ico'), 'wb') as f:
                    f.write(favicon_content)

                    return True
                
        else:
            faviconURL = URL+'/favicon.ico'
            print(domain," ", faviconURL)

            try:
                # Send an HTTP GET request to the Google favicon URL
                response = requests.get(faviconURL)

                    # Check if the request was successful
                if response.status_code == 200:
                        # Get the content of the favicon
                    favicon_content = response.content

                    only_brand_name, _ = os.path.splitext(domain)
                    logoFileName = only_brand_name + '.ico'
                    
                    logofile = os.path.join(logos_dir, f'{logoFileName}')

                    # Save the favicon image to a file
                    with open(logofile, 'wb') as file:
                        file.write(favicon_content)

                    return True

                else:

                    return False
                        

            except requests.exceptions.RequestException as e:
                with open(Exceptions, 'a') as file:
                    file.write(f'Error processing {URL}: {e}' + '\n')
        
    except Exception as e:
        with open(Exceptions, 'a') as file:
            file.write(f'Error processing {URL}: {e}' + '\n')
    
    return False


# def scrape_Screenshot(url, screenshots_dir, domain):
#     try:

#         # Set a timeout for page loading (adjust as needed)
#         driver.set_page_load_timeout(30)

#         # Navigate to the URL
#         driver.get(url)

#         # Scroll to the bottom of the page to load all content (optional)
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         # Get the full page height
#         full_page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

#         # Set the window size to match the full page height
#         driver.set_window_size(driver.get_window_rect()['width'], full_page_height)

#         # Save the screenshot to a file
#         screenshot_file = os.path.join(screenshots_dir, f'{domain}.png')
#         driver.save_screenshot(screenshot_file)

#         # Close the browser
#         driver.quit()

#         return True

#     except Exception as e:
        
#         print(f"Exception: {e}")
#         return False

if __name__ == '__main__':

    # Initialize a set to keep track of visited domains
    visited_domains = set()

    # Load the CSV file from the "tranco" directory, This is path according to the lab system

    csv_file_path = os.path.join('..', 'tranco', 'top-1m.csv')

    df = pd.read_csv(csv_file_path, header = None)

    counter = 0

    # Iterate through each row in the CSV
    for index, row in df.iterrows():

        # if counter == 10:
        #     break

        # Access the 2nd column using iloc (Also there are leading and trailing space in the domain name so remove them)
        domain = row.iloc[1].strip()
        print (domain)

        counter+=1
        
        # Check if the domain has already been visited in this run
        if domain in visited_domains:
            continue

        # Send an HTTP GET request to the URL
        url = 'https://' + domain

        # Run the scrape_favicon function
        found_favicon = scrape_Favicon(url, logos_dir, domain)

        # Run the capture_screenshot function
        # found_screenshot = scrape_Screenshot(url, screenshots_dir, domain)

        # Files to store the outputs for favicon and screenshot

        faviconOutput = os.path.join(outputs, 'favicon.txt')
        # screenshotOutput = os.path.join(outputs, 'screenshot.txt')

        if not found_favicon:
            with open(faviconOutput, 'a') as textLog:
                textLog.write(f'Favicon NOT found for {url}' + '\n')
        
        else:
            with open(faviconOutput, 'a') as textLog:
                textLog.write(f'Favicon found for {url}' + '\n')
        

        # if not found_screenshot:
        #     with open(screenshotOutput, 'a') as textLog:
        #         textLog.write(f'Screenshot NOT found for {url}' + '\n')

        # else:
        #     with open(screenshotOutput, 'a') as textLog:
        #         textLog.write(f'Screenshot found for {url}' + '\n')

        # Add the domain to the visited set to avoid duplicate requests
        visited_domains.add(domain)
        print(f"Counter: {counter}\n")

    print("Finished downloading favicons.")
