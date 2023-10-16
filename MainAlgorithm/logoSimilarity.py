from PIL import Image
import PIL
import cv2
import numpy as np
import os
import skimage
from skimage import io, color, img_as_ubyte
from skimage.metrics import structural_similarity as compare_ssim

import tensorflow as tf
import numpy as np
from PIL import Image

def resizeImages(img1, img2):
    # Resize the input images to the lowest resolution
    min_height = min(img1.shape[0], img2.shape[0])
    min_width = min(img1.shape[1], img2.shape[1])

    img1 = cv2.resize(img1, (min_width, min_height))
    img2 = cv2.resize(img2, (min_width, min_height))

    return img1, img2

def preprocess_image(image_path):
    # Load the image, convert to RGB, and resize to (224, 224)
    img = Image.open(image_path)
    img = img.convert('RGB')
    img = img.resize((85, 85))

    # Convert to a NumPy array and preprocess for ResNet-50
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.keras.applications.resnet50.preprocess_input(img)
    
    # Expand dimensions to match the shape (1, 224, 224, 3)
    img = np.expand_dims(img, axis=0)

    return img

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
    if mse!=0:
        psnr = 10 * np.log10((max_pixel_value ** 2) / mse)

    else:
        psnr = 100

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


def template_matching(image_path1, image_path2, reportFile, image2_ICO_path):
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    if image1 is None or image2 is None:
        return None
    
    img1, img2 = resizeImages(image1, image2)

    # Match the template in the main image using the cv2.TM_CCOEFF_NORMED method
    result = cv2.matchTemplate(image1, image2, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8 

    # Find all locations where the match exceeds the threshold
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))  # Reverse the coordinates

    # Calculate and return the similarity scores for each match
    similarity_scores = [result[loc[::-1]] for loc in locations]

    return similarity_scores


def CNN_similarity(image_path1, image_path2, reportFile, image2_ICO_path):
    # Load a pre-trained ResNet-50 model (without the top classification layer)

    # Pre-trained models (ResNet-50, ResNet-101, ResNet-152; VGG-16/19;  InceptionV3, InceptionResNetV2; DenseNet-121, DenseNet-169, )
    # base_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False)
    base_model = tf.keras.applications.VGG19(weights='imagenet', include_top=False)

    # Define input layers for the two images
    input_a = tf.keras.layers.Input(shape=(85, 85, 3))
    input_b = tf.keras.layers.Input(shape=(85, 85, 3))

    # Use the same base model for both inputs
    embedding_a = base_model(input_a)
    embedding_b = base_model(input_b)

    # Compute L2 distance between the two embeddings
    distance = tf.keras.layers.Lambda(lambda embeddings: tf.norm(embeddings[0] - embeddings[1], ord='euclidean', axis=1), 
                      output_shape=(1,))(inputs=[embedding_a, embedding_b])

    # Create a model that takes two input images and calculates the distance
    siamese_model = tf.keras.models.Model(inputs=[input_a, input_b], outputs=distance)

    # Load and preprocess the two images
    img1 = preprocess_image(image_path1)
    img2 = preprocess_image(image_path2)

    # Calculate the distance (difference) between the two images
    difference = siamese_model.predict([img1, img2])

    if difference.size == 1:
        similarity_percentage = difference.item()

    else:
        # Handle the case where difference contains multiple similarity values
        average_difference = difference.mean()  # Calculate the average similarity
        similarity_percentage = (1 - average_difference) * 100

    if similarity_percentage >= 75:
        with open (reportFile, 'a') as f:
            f.write(f"similarity score with {image2_ICO_path} according to CNN: {similarity_percentage:.2f}\n")

    return similarity_percentage

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
        image1_PNG_path = f"input_PNGs/{input_domain_name}.png"
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

        # similarity = ssim_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)

        """ 3. Peak Signal-to-Noise Ratio (PSNR) """

        PSNR = psnr_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)

        # similarity = PSNR

        """ 4. Histogram-based Similarity """

        # Performs very bad
        # similarity = histogram_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)

        """ 5. Template Matching """ # (Used to get the exact matching location), (threshold = 0.8, change it according to analysis)
        # similarity = template_matching(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)

        """ 6. CNNs """

        similarity = CNN_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)


        if similarity is not None and similarity >= 75:
            similar_logos[filename] = similarity  # Store the filename and similarity score in the dictionary
        
    return similar_logos