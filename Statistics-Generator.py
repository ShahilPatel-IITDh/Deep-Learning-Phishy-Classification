import os

# Define the path to the folder containing the .txt files
folder_path = "reports-openphish-100"

# Initialize counters
phishy_counter = 0
suspicious_counter = 0
legitimate_counter = 0
total_files = 0

# Function to check a single text file
def check_file(file_path):
    global phishy_counter, suspicious_counter, legitimate_counter, total_files

    total_files += 1

    with open(file_path, 'r') as file:
        for line in file:
            if "website is Phishy" in line:
                phishy_counter += 1
                break  # No need to continue searching in this file
            elif "website is Suspicious" in line:
                suspicious_counter += 1
                break
            elif "website is Legitimate" in line:
                legitimate_counter += 1
                break

# Walk through the directory and check each .txt file
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        if file_name.endswith(".txt"):
            file_path = os.path.join(root, file_name)
            check_file(file_path)

# Print the results
print("Total Files:", total_files)
print("Phishy Count:", phishy_counter)
print("Suspicious Count:", suspicious_counter)
print("Legitimate Count:", legitimate_counter)