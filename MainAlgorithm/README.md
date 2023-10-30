# Documentation for the main algorithm

## main.py

This Python script provides a comprehensive system for analyzing websites, capturing full-page screenshots, downloading favicons and assigning a weighted score to determine if a website is legitimate, suspicious, or potentially phishy.

### Features

    - **Full-Page Screenshot Capture**: Captures a full-page screenshot of a specified website.
    - **Input Box Detection**: Detects the presence or absence of input boxes on the web page.
    - **Frequent Terms Extraction**: Extracts the top 5 most occurring terms from the website's source code and screenshot.
    - **Domain Name Analysis**: Compares the input domain name to domains obtained from a search engine.
    - **Favicon Scraping**: Retrieves the website's favicon (site icon).
    - **Logo Similarity Detection**: Checks if the website's logo is similar to known logos in a database.
    - **Weighted Scoring**: Assigns a weighted score to determine the website's legitimacy.
    - **Logging**: Logs all results to provide detailed report for each URL.
  
### Usage

    1. Create a CSV file containing a list of URLs to be analyzed. (Can be executed for single URL as well)
    2. Run this script, Specify in the terminal whether you want to analyze a single URL or a list of URLs, in case of list of URLs specifying the path to the CSV file containing multiple URLs.
    3. The script will process each URL, and generate an analysis report.
    4. The report includes the weighted score and categorizes the website as legitimate, suspicious, or phishy.
    5. Detailed information, such as screenshot analysis, domain name analysis and logo similarity, is also included in the report.

### Dependencies

    - Python 3.x
    - Selenium: For web automation.
    - PIL (Python Imaging Library): For image processing.
    - Other Python libraries and modules, such as 'urllib.parse,' 'os,' 'time,' 'csv,' and 'logging.'

**Note**: Additional modules and functions are imported from separate Python files (e.g., 'screenshotCapture.py', 'UI_Detection.py', 'frequentTerms_Checking.py') to perform specific tasks.

The script's comprehensive analysis, including input box detection, frequent terms extraction, domain name checks, and logo similarity, helps users identify potentially fraudulent websites. The weighted scoring mechanism provides a quick assessment of website legitimacy, aiding security analysts, researchers, and developers in website evaluation and phishing detection.

### getLogo.py

This module will be called from main.py to fetch the favicon of the suspicious URL.

### screenshotCapture.py

This module will be called from main.py to fetch the screenshot of the webpage of the suspicious URL.

### UI_Detection.py

This module will be called from main.py to detect the presence of input boxes in the webpage screenshot. This uses the pytesseract library to perform OCR on the webpage screenshot. It checks for the presence of the following keywords in various languages (English, German, Spanish, Arabic, Hindi, French, Portuguese, Italian, Finnish, Swedish, Persian, Indonesian) in the OCR output:

- username
- password
- login
- sign in
- input
- log in
- submit
- email
- phone
- otp
- pin
- card
- cvv
- account
