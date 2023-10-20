import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import logging

logging.basicConfig(filename='faviconErrors.log', level=logging.ERROR)


# Define the list of allowed favicon formats
allowed_formats = ['.png', '.ico', '.jpeg', '.jpg', '.svg']

def scrape_favicon(URL, faviconFile, domain):

    print("Code entered the scrape_favicon function")

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    try:
        # Fetch the web page content
        response = requests.get(URL, headers=headers, timeout=5)
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Failed to fetch {URL}, status code: {response.status_code}")

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # List of favicon link types to check
        favicon_link_types = ['icon', 'apple-touch-icon', 'shortcut icon', 'mask-icon', 'fluid-icon', 'manifest', 'yandex-tableau-widget', 'apple-touch-startup-image', 'apple-touch-icon-precomposed', 'ICON', 'SHORTCUT ICON', 'APPLE-TOUCH-ICON', 'MANIFEST', 'MASK-ICON']

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

                _, extension = os.path.splitext(domain)
                
                if extension.lower() not in allowed_formats:
                    extension = '.ico'
                
                with open(faviconFile+extension, 'wb') as f:
                    f.write(favicon_content)
                
                return True
            
        else:
            # If no favicon link was found, try some common locations
            possible_favicon_locations = ['/favicon.ico', '/images/favicon.ico', '/img/favicon.ico', '/assets/favicon.ico']

            for location in possible_favicon_locations:
                faviconURL = urljoin(URL, location)
                print(domain, " ", faviconURL)

                try:
                    # Send an HTTP GET request to the Google favicon URL
                    response = requests.get(faviconURL)

                    # Check if the request was successful
                    if response.status_code == 200:
                        # Get the content of the favicon
                        favicon_content = response.content

                        # Save the favicon image to a file
                        with open(faviconFile, 'wb') as file:
                            file.write(favicon_content)

                        _, extension = os.path.splitext(domain)
                        
                        if extension.lower() not in allowed_formats:
                            extension = '.ico'
                        
                        with open(faviconFile + extension, 'wb') as file:
                            file.write(favicon_content)
                        
                        print("Code is about to exit the scrape_favicon function")

                        return True
                    
                    else:

                        print("Code is about to exit the scrape_favicon function")
                        return False

                except requests.exceptions.RequestException as e:
                    logging.error(f"RequestException for {URL}. Error: {str(e)}")
                    print("Code is about to exit the scrape_favicon function")

    except Exception as e:
        logging.error(f"Error processing {URL}. Error: {str(e)}")
        print("Code is about to exit the scrape_favicon function")