# Documentation for the main algorithm

## main.py

This is the main script which should be executed to get the results. This script will call the other modules to:

- Fetch the favicon of the suspicious URL.
- Screenshot of the webpage of the suspicious URL.
- Detect the presence of input boxes in the webpage screenshot
- Check the similarity between the favicon of suspicious URL and the favicons of the legitimate URLs.
- Check the similarity of the suspicious URL's domain with the domain found after performing google search of (suspicious domain + frequent terms in screenshot and page source of the suspicious URL).
- Classify the webpage as legitimate or phishy.

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
