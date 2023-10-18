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


def CNN_similarity(image_path1, image_path2, reportFile, image2_ICO_path):

    """
    Calculate image similarity using a Siamese CNN model based on VGG19 architecture.

    Parameters:
    - image_path1 (str): The file path to the first image.
    - image_path2 (str): The file path to the second image.
    - reportFile (str): The file path to the report where the similarity score will be saved.
    - image2_ICO_path (str): The path to the ICO image for reference in the report.

    Returns:
    - similarity_percentage (float): The similarity percentage between the two input images.

    Description:
    This function uses a Siamese Convolutional Neural Network (CNN) to measure the similarity between two input images.
    It uses a pre-trained VGG19 model for feature extraction and calculates the Euclidean distance between the embeddings of
    the two input images. Smaller the euclidean distance, higher the similarity between the two images.

    The similarity score is then calculated based on the distance, and a report is generated if the similarity percentage
    is greater than or equal to 75%. The report includes the image2_ICO_path and the calculated similarity score.

    Note: The choice of using the VGG19 architecture is arbitrary and you can use other pre-trained models based on your
    specific requirements.

    """
     
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
            f.write(f"similarity score with {image2_ICO_path} according to CNN (architecture-VGG19): {similarity_percentage:.2f}\n")

    return similarity_percentage

# ------------------------------------- This Function is the entry point of this module ------------------------------------- #

def detect_logo_similarity(input_domain_name, logoFile, logoDatabase, reportFile):


    print(f"The Logo file in detect_logo_similarity is {logoFile}")
    similar_logos = {}  # Dictionary to store similar logos

    os.makedirs("input_PNGs", exist_ok=True)
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

            # If the PNG image exists already then no need to convert it again
            if os.exists(image2_PNG_path):
                continue

            # Else convert the .ico file to .png format
            else:
                image2_ICO.convert('RGB').save(image2_PNG_path, format='PNG')

        except Exception as e:
            print(f"Skipping {filename} due to {e}.")
            continue  # Skip this image
    

        # Call the similarity functions 
        """ 1. CNNs ()"""

        similarity = CNN_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)


        if similarity is not None and similarity >= 75:
            similar_logos[filename] = similarity  # Store the filename and similarity score in the dictionary

    return similar_logos