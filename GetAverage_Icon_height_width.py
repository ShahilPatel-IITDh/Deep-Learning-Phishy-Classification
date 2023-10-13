from PIL import Image
import os

def calculate_average_image_dimensions(folder_path):
    total_height = 0
    total_width = 0
    image_count = 0

    errorCount = 0

    maxHeight = 0
    maxWidth = 0

    maxFile = ""

    # Check if the folder path exists
    if not os.path.exists(folder_path):
        return None
    

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):

        if image_count == 85000:
            break
        
        file_path = os.path.join(folder_path, filename)

        # Check if the file is an image (you can customize this check)
        if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.ico']):
            try:
                # Open the image and get its dimensions
                with Image.open(file_path) as img:
                    width, height = img.size

                    if width > maxWidth:
                        maxWidth = width
                        maxFile = filename

                    if height > maxHeight:
                        maxHeight = height
                        maxFile = filename

                    total_width += width
                    total_height += height
                    image_count += 1

            except Exception as e:
                errorCount+=1
                print(f"Error processing {filename}: {str(e)}")

    if image_count == 0:
        return None

    average_width = total_width / image_count
    average_height = total_height / image_count

    with open("average_dimensions.txt", "a") as f:
        f.write(f"{image_count}: {average_width}; {average_height}; {errorCount}\n")
    
    with open('max_dimensions.txt', 'a') as f:
        f.write(f"{image_count}: {maxHeight}; {maxWidth}; {maxFile}\n")

    return average_width, average_height, errorCount

# Provide the folder path containing images
folder_path = "/home/administrator/Desktop/Deep-Learning-Phishy-Classification/Logos"

average_dimensions = calculate_average_image_dimensions(folder_path)

if average_dimensions:
    print(f"Average Width: {average_dimensions[0]:.2f}")
    print(f"Average Height: {average_dimensions[1]:.2f}")
    print(f"Error Count: {average_dimensions[2]:.2f}")

else:
    print("No valid images found in the folder.")
