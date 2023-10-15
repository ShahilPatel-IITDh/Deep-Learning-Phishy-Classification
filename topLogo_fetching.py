import os
import shutil
import pandas as pd

# Define the input CSV file and the directories
csv_file = 'tranco/top-1m.csv'
source_directory = 'Logos'
target_directory = 'top_Logos_300'

# Create the target directory if it doesn't exist
if not os.path.exists(target_directory):
    os.mkdir(target_directory)

# Initialize a counter to keep track of the number of images processed
image_count = 0


df = pd.read_csv(csv_file, header = None)

for index, row in df.iterrows():

    if index == 3:
         break

    # Access the 2nd column using iloc (Also there are leading and trailing space in the domain name so remove them)
    domain = row.iloc[1].strip()

    # Remove whitespace from the string of domain and add ".ico" at the end
    image_name = domain + ".ico"

    # Check if the image file exists in the source directory
    source_path = os.path.join(source_directory, image_name)

    if os.path.exists(source_path):
        # Copy the image to the target directory
        target_path = os.path.join(target_directory, image_name)
        shutil.copy(source_path, target_path)
        image_count += 1
        print(f'Copied {image_name} to {target_directory}')

print(f'\nCopied {image_count} images to {target_directory}')
print("-----------------------------------------")
