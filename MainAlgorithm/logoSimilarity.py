from PIL import Image
import PIL
import cv2
import numpy as np
import os
import skimage
from skimage import io, color, img_as_ubyte
from skimage.metrics import structural_similarity as compare_ssim

def resizeImages(img1, img2):
    # Resize the input images to the lowest resolution
    min_height = min(img1.shape[0], img2.shape[0])
    min_width = min(img1.shape[1], img2.shape[1])

    img1 = cv2.resize(img1, (min_width, min_height))
    img2 = cv2.resize(img2, (min_width, min_height))

    return img1, img2


def mse_similarity(image_path1, image_path2, reportFile, image2_ICO_path):

    similar_logos = {}  # Dictionary to store similar logos

    # Load the input images
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    # Ensure img1 and img2 are valid images
    if img1 is None or img2 is None:
        return None

    similarity_scores = {}

    img1, img2 = resizeImages(img1, img2)

    mse = ((img1 - img2) ** 2).mean()

    similarity_percentage = (1-mse)*100
    
    # # Lower the MSE more is the Logo similarity
    if similarity_percentage >= 75:
        with open (reportFile, 'a') as f:
            f.write(f"similarity score with {image2_ICO_path} according to MSE: {similarity_percentage:.2f}\n")

    return mse

def ssim_similarity(image_path1, image_path2, reportFile, image2_ICO_path):
    # Read the input images
    image1 = io.imread(image_path1)
    image2 = io.imread(image_path2)

    img1, img2 = resizeImages(image1, image2)

    # Convert images to grayscale if they are in color
    if len(img1.shape) > 2:
        img1 = color.rgb2gray(img1)

    if len(img2.shape) > 2:
        img2 = color.rgb2gray(img2)
    
    # Calculate SSIM with specified data_range
    data_range = 1.0  # Assuming a data range of 1.0 for floating-point images
    ssim_score = compare_ssim(img1, img2, data_range=data_range)
    
    # Higher the SSIM more is the Logo similarity
    ssim_score = ssim_score * 100

    if ssim_score >= 75:
        with open (reportFile, 'a') as f:
            f.write(f"similarity score with {image2_ICO_path} according to SSIM: {ssim_score:.2f}\n")

    return ssim_score


# In PSNR, a higher value indicates higher image similarity and better image quality
def psnr_similarity(image_path1, image_path2, reportFile, image2_ICO_path):
    # Load the images
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    img1, img2 = resizeImages(image1, image2)

    # Calculate the Mean Squared Error (MSE)
    mse = ((img1 - img2) ** 2).mean()

    # Maximum possible pixel value
    max_pixel_value = 255.0

    # Calculate PSNR
    psnr = 10 * np.log10((max_pixel_value ** 2) / mse)

    if psnr >= 75:
        with open (reportFile, 'a') as f:
            f.write(f"similarity score with {image2_ICO_path} according to PSNR: {psnr:.2f}\n")

    return psnr


def histogram_similarity(image_path1, image_path2, reportFile, image2_ICO_path):
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    if image1 is None or image2 is None:
        return None

    img1, img2 = resizeImages(image1, image2)

    # Convert the images to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculate histograms
    hist1 = cv2.calcHist([img1_gray], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2_gray], [0], None, [256], [0, 256])

    # Normalize the histograms
    hist1 /= hist1.sum()
    hist2 /= hist2.sum()

    # Calculate the Bhattacharyya coefficient
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)*100

    if similarity >= 99:
        with open (reportFile, 'a') as f:
            f.write(f"similarity score with {image2_ICO_path} according to Histogram Bhattacharya: {similarity:.2f}\n")

    return similarity


# ------------------------------------- This Function is the entry point of this module ------------------------------------- #

def detect_logo_similarity(input_domain_name, logoFile, logoDatabase, reportFile):

    print(f"The Logo file in detect_logo_similarity is {logoFile}")
    similar_logos = {}  # Dictionary to store similar logos

    os.makedirs("output_PNGs", exist_ok=True)
    os.makedirs("Database_PNGs", exist_ok=True)

    try:
        #  Convert the logoFile to a valid image
        image1_ICO = Image.open(logoFile)

        # Convert the .ico image to another format (e.g., .png)
        image1_PNG_path = f"output_PNGs/{input_domain_name}.png"
        image1_ICO.convert('RGB').save(image1_PNG_path, format='PNG')
        
    except Exception as e:
        print(f"Skipping {input_domain_name} due to {e}.")
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

        except Exception as e:
            print(f"Skipping {filename} due to {e}.")
            continue  # Skip this image
    

        # Call the similarity functions 

        """ 1. Mean Squared Error (MSE) """
        mse = mse_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)
        # similarity%
        similarity = (1-mse)*100


        """ 2. Structural Similarity Index (SSIM) """

        similarity = ssim_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)

        """ 3. Peak Signal-to-Noise Ratio (PSNR) """

        similarity = psnr_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)

        """ 4. Histogram-based Similarity """

        # Performs very bad
        # similarity = histogram_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)

        if similarity is not None and similarity >= 75:
            similar_logos[filename] = similarity  # Store the filename and similarity score in the dictionary
        
    return similar_logos