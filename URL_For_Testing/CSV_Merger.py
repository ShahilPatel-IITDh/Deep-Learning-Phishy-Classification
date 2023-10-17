import csv

# List of CSV files you want to merge
csv_files = ["phishTankDatabase.csv", "Open-Phish-Database.csv"]

# Output file
output_file = "merged_URLs.csv"

# Iterate through the list of CSV files and merge them into a single column
merged_data = []

for file in csv_files:
    with open(file, 'r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            merged_data.extend(row)

# Save the merged data to a new CSV file with a single column
with open(output_file, 'w', newline='') as output_csv:
    writer = csv.writer(output_csv)
    for item in merged_data:
        writer.writerow([item])

print("CSV files merged into a single column and saved as 'merged_URLs.csv'.")