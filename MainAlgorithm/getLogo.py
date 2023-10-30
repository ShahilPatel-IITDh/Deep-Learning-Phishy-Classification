"""
Favicon Scraper Documentation

This Python code is a script that scrapes and downloads a website's favicon (shortcut icon) from the given URL.
The favicon is typically a small image that represents a website and is displayed in a web browser's address bar,
tabs, and bookmarks. The script attempts to locate and download the favicon from various possible sources, including
HTML metadata and common default paths.

Usage:
To use this script, call the 'scrape_favicon' function with the following parameters:
- URL: The URL of the website from which the favicon is to be scraped.
- faviconFile: The file path where the downloaded favicon will be saved.
- domain: The domain name of the website.

Example:
scrape_favicon("https://example.com", "example_favicon", "example.com")

Dependencies:
- Python 3.x
- The 'os' module
- The 'requests' library for making HTTP requests.
- The 'BeautifulSoup' library for parsing HTML content.
- The 'urllib.parse' module for URL parsing.
- Logging functionality for error handling.

Functions:
1. scrape_favicon(URL, faviconFile, domain)
    - URL: The URL of the website from which to scrape the favicon.
    - faviconFile: The path where the downloaded favicon will be saved.
    - domain: The domain name of the website.
    - Returns: True if the favicon was successfully downloaded, otherwise False.

The script fetches the web page content, parses it to locate the favicon URL in the HTML metadata (rel='icon'; 'apple-touch-icon'; 'shortcut icon'; 'mask-icon'; 'fluid-icon'; 'manifest'; 'yandex-tableau-widget'; 'apple-touch-startup-image'; 'apple-touch-icon-precomposed'; 'ICON'; 'SHORTCUT ICON'; 'APPLE-TOUCH-ICON'; 'MANIFEST'; 'MASK-ICON'),
downloads the favicon, and saves it to the specified file. If the favicon is not found in the HTML metadata, it attempts
to download it from common default locations like "/favicon.ico".

Additionally, if the file extension of the domain name does not match any of the allowed favicon formats (e.g., .png, .ico),
it defaults to .ico format.

Note:
- Ensure that the required libraries are installed before using this script.
- Logging is used for error handling and can be configured using the 'logging' library settings.
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import logging

logging.basicConfig(filename='faviconErrors.log', level=logging.ERROR)


# Define the list of allowed favicon formats
allowed_formats = ['.png', '.ico', '.jpeg', '.jpg', '.svg']

def scrape_favicon(URL, faviconFile, domain):

    """
    Scrape the favicon from a given website URL and save it to a file.

    :param URL: The URL of the website to scrape the favicon from.
    :param faviconFile: The file path where the downloaded favicon will be saved.
    :param domain: The domain name of the website.

    :return: True if the favicon was successfully downloaded, otherwise False.
    """

    print("--Code entered the scrape_favicon function")
    print("|")

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
                        
                        print("|")
                        print("--Code is about to exit the scrape_favicon function\n")

                        return True
                    
                    else:
                        
                        print("|")
                        print("--Code is about to exit the scrape_favicon function\n")
                        return False

                except requests.exceptions.RequestException as e:
                    logging.error(f"RequestException for {URL}. Error: {str(e)}")
                    
                    print("|")
                    print("--Code is about to exit the scrape_favicon function\n")

    except Exception as e:
        logging.error(f"Error processing {URL}. Error: {str(e)}")

        print("|")
        print("--Code is about to exit the scrape_favicon function\n")