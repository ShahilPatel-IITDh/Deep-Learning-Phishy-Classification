# Favicon and Screenshot Scraping Script

This script is designed to scrape and download favicons (website icons) from a list of domains stored in a CSV file. It also has the capability to capture screenshots of websites but this feature is currently disabled. The script performs the following tasks:

1. Creates directories for storing logos (favicons), screenshots, and log files if they do not exist.
2. Visits websites listed in a CSV file.
3. Scrapes the favicon for each website and saves it as an `.ico` file in the logos directory.
4. Records the results (whether a favicon was found or not) in an output file.

## Prerequisites

Make sure you have the following Python libraries installed:

- `os`
- `requests`
- `pandas`
- `BeautifulSoup` (from `bs4`)
- `urllib.parse`
- `time`

You can install these libraries using `pip` if you haven't already:

```bash
pip install requests pandas beautifulsoup4
```

## Usage
```python
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

# Define directory paths
logos_dir = os.path.join('..', 'Logos')
screenshots_dir = os.path.join('..', 'Screenshots')
outputs = os.path.join('..', 'outputs')
```

- logos_dir: Directory for storing downloaded favicons.
- screenshots_dir: Directory for storing screenshots (currently unused).
- outputs: Directory for storing log files and other outputs.

## Run the script

```bash
python logoFetcher.py
```

## Script Workflow
1. The script creates the necessary directories (Logos, Screenshots, and Outputs) if they do not already exist.
2. It loads a CSV file containing a list of domains to be visited.
3. It iterates through each domain in the CSV file and performs the following tasks:
   - Sends an HTTP GET request to the domain's URL.
   - Scrapes the favicon from the website and saves it as an .ico file in the logos directory.
   - Records the results (whether a favicon was found or not) in an output file.
4. The script avoids duplicate requests by keeping track of visited domains.

## Note
Exceptions encountered during the process are logged in an **Exceptions.txt** file.
Customize the script as needed for your specific use case.