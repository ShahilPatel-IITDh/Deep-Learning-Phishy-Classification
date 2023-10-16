from PIL import Image
import PIL
import cv2
import numpy as np
import os

from skimage import io, color, img_as_ubyte
from skimage.metrics import structural_similarity as compare_ssim

def mse_similarity(image_path1, image_path2, reportFile, image2_ICO_path):

    similar_logos = {}  # Dictionary to store similar logos

    # Load the input images
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    # Ensure img1 and img2 are valid images
    if img1 is None or img2 is None:
        return None

    similarity_scores = {}

    # Resize the input images to the lowest resolution
    min_height = min(img1.shape[0], img2.shape[0])
    min_width = min(img1.shape[1], img2.shape[1])

    img1 = cv2.resize(img1, (min_width, min_height))
    img2 = cv2.resize(img2, (min_width, min_height))

    mse = ((img1 - img2) ** 2).mean()
    
    # # Lower the MSE more is the Logo similarity
    # if mse < 0.85:
    #     with open (reportFile, 'a') as f:
    #         f.write(f"Similarity with and {image2_ICO_path} are similar with an MSE score of {mse:.2f}\n")

    return mse

def detect_logo_similarity(input_domain_name, logoFile, logoDatabase, reportFile):
    similar_logos = {}  # Dictionary to store similar logos

    os.makedirs("output_PNGs", exist_ok=True)
    os.makedirs("Database_PNGs", exist_ok=True)

    try:
        #  Convert the logoFile to a valid image
        image1_ICO = Image.open(logoFile)

        # Convert the .ico image to another format (e.g., .png)
        image1_PNG_path = f'output_PNGs/{input_domain_name}.png'
        image1_ICO.convert('RGB').save(image1_PNG_path, format='PNG')
        
    except PIL.UnidentifiedImageError:
        print(f"Skipping {input_domain_name} due to unidentified image file.")
        return  # Skip this image

    # Ensure the folder path exists
    if not os.path.exists(logoDatabase) or not os.path.isdir(logoDatabase):
        return {}
    
    # Load the input image
    for filename in os.listdir(logoDatabase):
        image2_ICO_path = os.path.join(logoDatabase, filename)

        try:
            # Load the ICO image using PIL
            image2_ICO = Image.open(image2_ICO_path)

            # Convert the .ico image to another format (e.g., .png)
            image2_PNG_path = f'Database_PNGs/{filename}.png'  # Use a different path for each image
            image2_ICO.convert('RGB').save(image2_PNG_path, format='PNG')

        except PIL.UnidentifiedImageError:
            print(f"Skipping {filename} due to unidentified image file.")
            continue  # Skip this image
    

        # Call the similarity functions
        similarity = mse_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)

        # similarity = compare_ssim(image1_PNG_path, image2_PNG_path)

        if similarity is not None and similarity < 0.25:
            similar_logos[filename] = similarity  # Store the filename and similarity score in the dictionary
        
    return similar_logos