# Various algorithms will be used to compare the similarity of two logos, so that we can check which one will give us most accurate results.

# 1. Mean Squared Error (MSE): MSE measures the average squared difference between pixel values in two images. It's simple to implement but might not work well for complex image comparisons.

import cv2
import os

def mse_similarity(image_path1, folder_path):
    # Load the input image
    img1 = cv2.imread(image_path1)

    # Ensure the folder path exists
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return {}

    similarity_scores = {}

    # Resize the input image to the lowest resolution within the folder
    min_height = img1.shape[0]
    min_width = img1.shape[1]

    for filename in os.listdir(folder_path):
        image_path2 = os.path.join(folder_path, filename)
        img2 = cv2.imread(image_path2)

        # Ensure img2 is a valid image
        if img2 is not None:
            min_height = min(min_height, img2.shape[0])
            min_width = min(min_width, img2.shape[1)

    img1 = cv2.resize(img1, (min_width, min_height))

    # Calculate the Mean Squared Error for each image in the folder
    for filename in os.listdir(folder_path):
        image_path2 = os.path.join(folder_path, filename)
        img2 = cv2.imread(image_path2)

        # Ensure img2 is a valid image
        if img2 is not None:
            img2 = cv2.resize(img2, (min_width, min_height))
            mse = ((img1 - img2) ** 2).mean()

            if mse < 0.2:  # Adjust the threshold as needed
                similarity_scores[filename] = mse

    return {k: v for k, v in similarity_scores.items() if v > 0.8}