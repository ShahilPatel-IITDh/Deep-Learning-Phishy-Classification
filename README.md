# Deep-Learning-Phishy-Classification
This repository is to store the code to fetch the Logos of Legitimate domains, and their webpage screenshots, models, dataset and documentation for the classification of the Phishy Websites using deep learning techniques.

## References:
- PhishPedia

## Directory structure
```
.
├── Logo_Fetching
│   ├── logoFetcher.py

├── README.md

├── Logos
│   ├── Logos of Legitimate Domains

├── Outputs
│   ├── Log Files of the Logo Fetching code and the exceptions occurred

├── tranco
│   ├── CSV file containing the top 1 million domains

├── MainAlgorithm
│   ├── main.py (The script which should be executed to get the results)
│   |── getLogo.py (Module to fetch the logo of the domain, will be called from main.py)
│   |── screenshotCapture.py (Module to fetch the full page screenshot of the domain, will be called from main.py)
│   |── UI_Detection.py (Module which will be called from main.py to detect the presence of input boxes in the webpage screenshot)

├── URL_For_Testing
│   ├── scrappingCode.py (Code to fetch the URLs from PhishTank and store the URLs in a CSV file which can be used for testing our algorithm)
│   ├── phishTankDatabase.csv (CSV file containing the URLs fetched from PhishTank)



```