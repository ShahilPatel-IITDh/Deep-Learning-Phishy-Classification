# Documentation for the main algorithm

## main.py

This Python script provides a comprehensive system for analyzing websites, capturing full-page screenshots, downloading favicons and assigning a weighted score to determine if a website is legitimate, suspicious, or potentially phishy.

### Features of main.py

- **Full-Page Screenshot Capture**: Captures a full-page screenshot of a specified website.
- **Input Box Detection**: Detects the presence or absence of input boxes on the web page.
- **Frequent Terms Extraction**: Extracts the top 5 most occurring terms from the website's source code and screenshot.
- **Domain Name Analysis**: Compares the input domain name to domains obtained from a search engine.
- **Favicon Scraping**: Retrieves the website's favicon (site icon).
- **Logo Similarity Detection**: Checks if the website's logo is similar to known logos in a database.
- **Weighted Scoring**: Assigns a weighted score to determine the website's legitimacy.
- **Logging**: Logs all results to provide detailed report for each URL.
  
### Usage of main.py

1. Create a CSV file containing a list of URLs to be analyzed. (Can be executed for single URL as well)
2. Run this script, Specify in the terminal whether you want to analyze a single URL or a list of URLs, in case of list of URLs specifying the path to the CSV file containing multiple URLs.
3. The script will process each URL, and generate an analysis report.
4. The report includes the weighted score and categorizes the website as legitimate, suspicious, or phishy.
5. Detailed information, such as screenshot analysis, domain name analysis and logo similarity, is also included in the report.

### Dependencies of main.py

- Python 3.x
- Selenium: For web automation.
- PIL (Python Imaging Library): For image processing.
- Other Python libraries and modules, such as 'urllib.parse,' 'os,' 'time,' 'csv,' and 'logging.'

**Note**: Additional modules and functions are imported from separate Python files (e.g., 'screenshotCapture.py', 'UI_Detection.py', 'frequentTerms_Checking.py') to perform specific tasks.

The script's comprehensive analysis, including input box detection, frequent terms extraction, domain name checks, and logo similarity, helps users identify potentially fraudulent websites. The weighted scoring mechanism provides a quick assessment of website legitimacy, aiding security analysts, researchers, and developers in website evaluation and phishing detection.

## getLogo.py

This Python script provides a utility for scraping the favicon (site icon) from a given website URL and saving it to a file. It is designed for extracting the favicon of a website, which is often used for branding and identification.

### Features of getLogo.py

- Scrape Favicon: Given a website URL, the script attempts to locate and download the website's favicon.
- Supported Favicon Formats: The script supports common favicon formats, including .png, .ico, .jpeg, .jpg, and .svg.
- Retry on Common Locations: If the favicon link is not found in the HTML content, the script attempts to fetch the favicon from common locations (e.g., '/favicon.ico', '/images/favicon.ico').

### Usage of getLogo.py

1. Import this script into your project.
2. Call the `scrape_favicon` function, providing the website URL, the file path to save the favicon, and the website's domain name as parameters.
3. The function will attempt to scrape the favicon and return True if successful, otherwise, it returns False.

### Dependencies of getLogo.py

- Python 3.x
- requests: For making HTTP requests to the website and fetching the favicon content.
- BeautifulSoup: For parsing the HTML content of the website and locating favicon links.
- Other Python modules and functions, such as 'os' and 'logging.'

## screenshotCapture.py

This Python script provides a utility for capturing a full-page screenshot of a given website URL using Selenium WebDriver with Chrome. The captured screenshot is then saved to a specified file.

### Features of screenshotCapture.py

- Capture Screenshot: Given a website URL, the script captures a full-page screenshot of the website's content.
- Headless Mode: The script can operate in headless mode, meaning it runs in the background without a visible browser window.
- Handling WebDriver Exceptions: It handles WebDriver exceptions, such as "ERR_NAME_NOT_RESOLVED," which can occur due to network issues or URL resolution problems.
- Scroll and Stitch: The script automatically scrolls through the entire webpage, capturing multiple screenshots and stitching them together to create a full-page screenshot.
- Error Logging: Errors, including WebDriver exceptions and general exceptions, are logged to a log file using the Python 'logging' module.

### Usage of screenshotCapture.py

1. Import this script into your project.
2. Call the `capture_full_page_screenshot` function, providing the website URL and the file path to save the screenshot as parameters.
3. The function will initiate a headless Chrome browser, capture the screenshot, and save it to the specified file.
4. Log messages are generated during the process to track the status and any encountered errors.

### Dependencies

- Python 3.x
- Selenium: For web automation, including taking screenshots.
- Pillow (PIL): For image processing and handling the screenshots.
- Logging: For error logging and status messages.

## UI_Detection.py

This Python script provides a utility for detecting input boxes in a screenshot image. The purpose is to identify the presence of input fields in a given screenshot.

### Features of UI_Detection.py

- Input Box Detection: The script processes the screenshot, applies image processing techniques to highlight potential input boxes, and checks for keywords that indicate the presence of input fields.
- Keyword Detection: The script searches for keywords related to input boxes in multiple languages (English, German, Spanish, Arabic, Hindi, French, Portuguese, Italian, Finnish, Swedish, Persian, Indonesian) in the extracted text using Tesseract OCR.
- Flexibility: The script can be easily extended with additional keywords or customized for specific use cases.

### Usage of UI_Detection.py

1. Import this script into your project.
2. Call the `detect_input_box` function, providing the file path of the screenshot image as a parameter.
3. The function will process the screenshot, analyze it for input boxes, and return a result code: -1 if input boxes are detected, 1 if no input boxes are detected.
4. You can customize the list of keywords for input box detection as needed.

### Dependencies of UI_Detection.py

- Python 3.x
- OpenCV (cv2): For image processing and handling screenshots.
- NumPy: For numerical and array operations.
- Pytesseract: For Optical Character Recognition (OCR) to extract text from the screenshot.

## Frequent Terms Checking

This Python script contains two text analysis utility functions that assist in processing and extracting textual information from images and websites.

### Utility 1: Preprocess Image for Text Extraction

- `preprocess_image(image_path)`: Preprocesses an image to enhance text for extraction. The image is opened using OpenCV, converted to grayscale, thresholded, and colors are inverted to make text black on a white background. Returns the preprocessed PIL image.

### Utility 2: Extract Top Terms from Screenshot

- `extract_top_terms_from_screenshot(domain_name, screenshot_path)`: Extracts the top 5 terms from a screenshot using OCR and text analysis.
- Parameters:
  - `domain_name` (optional): The domain name associated with the screenshot.
  - `screenshot_path`: The file path of the screenshot image.
- Returns a list of the top 5 most common terms (words) in the screenshot.

### Utility 3: Extract Top Terms from Website

- `get_top_terms_from_website(url)`: Extracts the top 5 terms from the text content of a website.
- Parameter:
  - `url`: The URL of the website to extract top terms from.
- Returns a list of the top 5 most common terms (words) in the website's text content.

### Features of frequentTerms_Checking.py

- Image preprocessing to enhance text.
- Text extraction and tokenization from images and websites.
- Removal of common stopwords.
- Counting word occurrences and extraction of the top terms.

### Dependencies of frequentTerms_Checking.py

- Python 3.x
- OpenCV (cv2): For image preprocessing.
- NumPy: For numerical and array operations.
- Pytesseract: For Optical Character Recognition (OCR) to extract text from images.
- Requests: For sending HTTP GET requests to websites.
- BeautifulSoup: For parsing HTML content from websites.

## domainName_Difference

This Python script contains a utility function to check the similarity between two domain names using the Levenshtein distance algorithm. It calculates a similarity score as a percentage based on the Levenshtein distance between the domain names.

### Utility: Check Domain Similarity

- `check_Domain_similarity(inputDomain, similarDomain)`: Compares the similarity between two domain names.
- Parameters:
  - `inputDomain`: The first domain name for comparison.
  - `similarDomain`: The second domain name for comparison.
- Returns a similarity score as a percentage based on the Levenshtein distance.

### Features of domainName_Difference.py

- Utilizes the Levenshtein distance algorithm to measure the difference between domain names.
- Returns a similarity score representing the similarity between domain names as a percentage.

### Dependencies of domainName_Difference.py

- Python 3.x
- Levenshtein: A Python package used to calculate Levenshtein distances between strings.

## Search_Engine.py

This Python script performs a Google search with a specified domain and search terms and extracts the top domains from the search results. The script utilizes Selenium and Chrome WebDriver to automate the search process.

Function: `google_search(domain, search_terms, reportFile)`

- Parameters:
  - `domain`: The domain used in the search query.
  - `search_terms`: A list of search terms to be added to the query.
  - `reportFile`: The file where search-related information is logged.

- Returns a list of the top domains from the search results.

### Features of Search_Engine.py

- Utilizes Selenium for web automation.
- Supports custom user agents for browsing.
- Searches Google with a combination of domain and search terms.
- Extracts the top domains from the search results (usually the top 3 results).

### Dependencies for Search_Engine.py

- Python 3.x
- Selenium: A Python package used for web automation.
- Chrome WebDriver: A WebDriver for the Google Chrome browser.

### Usage

- The `google_search` function is called with a domain, search terms, and a report file path.
- It performs a Google search, logs user agent information, and extracts top domains.

## Logo_Similarity

The detect_logo_similarity function is designed to compare an input domain's logo image with a database of logo images. It calculates the similarity using the Structural Similarity Index (SSIM) metric.

Input Parameters:

- input_domain_name (str): The name of the input domain.
- logoFile (str): The file path of the input domain's logo image.
- logoDatabase (str): The folder path containing a database of logo images.
- reportFile (str): The file where the results and report will be written.

Output:

- A dictionary containing filenames of similar logos as keys and their similarity scores as values.
