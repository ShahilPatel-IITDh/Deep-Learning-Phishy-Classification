import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

# Create the Logos directory if it doesn't exist in the Logo_fetching directory
logos_dir = os.path.join('..', 'Top_Logos_200')
outputs = os.path.join('..', 'outputs')

# Make the directory to store Logos if it doesn't exist
if not os.path.exists(logos_dir):
    os.mkdir(logos_dir)

# Make the directory to store outputs if it doesn't exist
if not os.path.exists(outputs):
    os.mkdir(outputs)

Exceptions = os.path.join(outputs, 'Exceptions.txt')

# Define the list of allowed favicon formats
allowed_formats = ['.png', '.ico', '.jpeg', '.jpg', '.svg']

def scrape_Favicon(URL, Favicons_Directory, domain):

    try:
        # Fetch the web page content
        response = requests.get(URL, headers=headers, timeout=5)
        
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

        if favicon_URL:
            favicon_response = requests.get(favicon_URL)
        
            if favicon_response.status_code == 200:
                favicon_content = favicon_response.content
                _, extension = os.path.splitext(domain)
                
                if extension.lower() not in allowed_formats:
                    extension = '.ico'
                
                with open(os.path.join(Favicons_Directory, domain + extension), 'wb') as f:
                    f.write(favicon_content)
                
                return True
                
        else:
            faviconURL = URL + '/favicon.ico'
            print(domain, " ", faviconURL)

            try:
                # Send an HTTP GET request to the Google favicon URL
                response = requests.get(faviconURL)

                # Check if the request was successful
                if response.status_code == 200:
                    # Get the content of the favicon
                    favicon_content = response.content

                    _, extension = os.path.splitext(domain)
                    
                    if extension.lower() not in allowed_formats:
                        extension = '.ico'
                    
                    with open(os.path.join(Favicons_Directory, domain + extension), 'wb') as file:
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

if __name__ == '__main__':
    # Initialize a set to keep track of visited domains
    visited_domains = set()

    # Load the CSV file from the "tranco" directory
    csv_file_path = os.path.join('..', 'tranco', 'top-1m.csv')

    df = pd.read_csv(csv_file_path, header=None)

    counter = 0

    # Iterate through each row in the CSV
    for index, row in df.iterrows():
        if counter == 220:
            break

        # Access the 2nd column using iloc (Also there are leading and trailing spaces in the domain name so remove them)
        domain = row.iloc[1].strip()
        print(domain)
        counter += 1
        
        # Check if the domain has already been visited in this run
        if domain in visited_domains:
            continue

        # Send an HTTP GET request to the URL
        url = 'https://' + domain

        # Run the scrape_favicon function
        found_favicon = scrape_Favicon(url, logos_dir, domain)

        # Add the domain to the visited set to avoid duplicate requests
        visited_domains.add(domain)
        print(f"Counter: {counter}\n")

    print("Finished downloading favicons.")