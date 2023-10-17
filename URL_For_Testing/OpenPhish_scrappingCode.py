import requests
import csv

openPhish_url = "https://openphish.com/feed.txt"

line_limit = 50  # Set the number of lines you want to retrieve
output_CSV = "Open-Phish-Database.csv"  # Name of the output CSV file

try:
    response = requests.get(openPhish_url)
    if response.status_code == 200:
        lines = response.text.split('\n')

        with open(output_CSV, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            for i, line in enumerate(lines[:line_limit]):
                writer.writerow([line])

            print(f"{line_limit} lines written to {output_CSV}")

    else:
        print("Failed to retrieve the content. Status code:", response.status_code)

except requests.exceptions.RequestException as e:
    print("An error occurred:", e)