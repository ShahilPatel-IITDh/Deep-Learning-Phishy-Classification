from PIL import Image
import os
import skimage
from skimage import io, color, img_as_ubyte, transform
from skimage.metrics import structural_similarity as ssim



def structural_similarity(image_path1, image_path2, reportFile, image2_ICO_path):

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
    # base_model = tf.keras.applications.VGG19(weights='imagenet', include_top=False)

    # base_model = tf.keras.applications.ResNet101V2(weights='imagenet', include_top=False)


    # img1 = preprocess_image(image_path1)
    # img2 = preprocess_image(image_path2)

    # # Get feature vectors from the base model
    # features1 = base_model.predict(img1)
    # features2 = base_model.predict(img2)

    # # Reshape the feature vectors
    # features1 = features1.reshape(features1.shape[0], -1)
    # features2 = features2.reshape(features2.shape[0], -1)

    # # Normalize the feature vectors
    # features1 /= np.linalg.norm(features1, axis=1)[:, np.newaxis]
    # features2 /= np.linalg.norm(features2, axis=1)[:, np.newaxis]

    # # Calculate the similarity score (cosine similarity)
    # similarity = np.dot(features1, features2.T)

    # # Scale the similarity score to the 0-100 range
    # similarity_percent = (similarity + 1) * 50

    # # Ensure the score is within the 0-100 range
    # similarity_percent = max(0, min(similarity_percent, 100))

    #  # Convert to integer
    # similarity_percent = int(similarity_percent)

    # if similarity_percent >= 96:
    #     with open (reportFile, 'a') as f:
    #         f.write(f"similarity score with {image2_ICO_path} according to CNN (architecture-VGG19): {similarity_percent:.2f}\n")

    # return similarity_percent

    # ------------------------------------- Structural Similarity detection  ------------------------------------- #

    """
    This code is used to calculate the structural similarity between two images. It follows a series of steps
    to preprocess and compare two images. The primary goal is to check whether the images are similar based on
    the Structural Similarity Index (SSIM).

    Usage:
    1. Load the images from specified file paths.
    2. Convert the images to grayscale if they are not already.
    3. Resize both images to a target shape (default is 224x224).
    4. Normalize the pixel values of the images to be in the range [0, 1].
    5. Calculate the SSIM (Structural Similarity Index) between the two images.
    6. If the similarity is greater than or equal to 75, it is written in the report.

    Parameters:
    - `image_path1`: File path to the first image.
    - `image_path2`: File path to the second image.
    - `reportFile`: File to write the similarity report.
    - `image2_ICO_path`: Path to the second image for reporting purposes.

    Returns:
    - `similarity_percent`: The similarity score as a percentage.
    """

    # Load the images
    image1 = io.imread(image_path1)
    image2 = io.imread(image_path2)

    # Convert images to grayscale if they are not already
    if image1.shape[-1] > 1:
        image1 = color.rgb2gray(image1)
    if image2.shape[-1] > 1:
        image2 = color.rgb2gray(image2)

    # Resize the images to the same shape (Here we took 75x75 as the average shape of the favicons present in the database is 68 x 68 so we took a little bigger size)
    target_shape = (75, 75)
    image1 = transform.resize(image1, target_shape)
    image2 = transform.resize(image2, target_shape)

    # Ensure pixel values are in the range [0, 1]
    image1 = image1 / image1.max()
    image2 = image2 / image2.max()

    # Calculate SSIM between the two images
    similarity = ssim(image1, image2, data_range=1.0)

    if similarity >= 75:
        with open (reportFile, 'a') as f:
            f.write(f"similarity score with {image2_ICO_path} according to SSIM: {similarity:.2f}\n")

    return similarity*100

# ------------------------------------- This Function is the entry point of this module ------------------------------------- #

def detect_logo_similarity(input_domain_name, logoFile, logoDatabase, reportFile):

    # print(f"The Logo file in detect_logo_similarity is {logoFile}")
    similar_logos = {}  # Dictionary to store similar logos

    os.makedirs("Input-PNGs-openphish-100", exist_ok=True)
    os.makedirs("Database-PNGs-openphish-100", exist_ok=True)

    try:
        #  Convert the logoFile to a valid image
        with Image.open(logoFile) as img:
            # Convert to RGB mode (required for saving as PNG)
            img = img.convert("RGB")

            image1_PNG_path = f"Input-PNGs-openphish-100/{input_domain_name}.png"

            # Save the image as a PNG file
            img.save(image1_PNG_path, 'PNG')
        
    except Exception as e:
        # print(f"Skipping {input_domain_name} due to {e}.")
        return  # Skip this image

    # Ensure the folder path exists
    if not os.path.exists(logoDatabase) or not os.path.isdir(logoDatabase):
        # print("LogoDatabase folder does not exist.")
        return {}
    
    # Load the input image
    for filename in os.listdir(logoDatabase):
        # print(f"Processing {filename} in Logo Database...")
        image2_ICO_path = os.path.join(logoDatabase, filename)
        
        try:
            # Load the ICO image using PIL
            image2_ICO = Image.open(image2_ICO_path)

            # Convert the .ico image to another format (e.g., .png)
            image2_PNG_path = f'Database-PNGs-openphish-100/{filename}.png'  # Use a different path for each image
            
            if os.path.isfile(image2_PNG_path):
                # If the image has already been converted, then check it's similarrity with the input image

                # Call the similarity functions 
                # """ 1. CNNs ()"""

                """2. SSIM (Structural Similarity Index)"""

                similarity = structural_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)

                if similarity is not None and similarity >= 75:
                    similar_logos[filename] = similarity  # Store the filename and similarity score in the dictionary

                continue
            
            else:
                image2_ICO.convert('RGB').save(image2_PNG_path, format='PNG')
                
                # Convert the image and then feed the image to the image similarity functions
                # Call the similarity functions 
                # """ 1. CNNs ()"""

                """2. SSIM (Structural Similarity Index)"""
                similarity = structural_similarity(image1_PNG_path, image2_PNG_path, reportFile, image2_ICO_path)

                if similarity is not None and similarity >= 96:
                    similar_logos[filename] = similarity  # Store the filename and similarity score in the dictionary
                    

        except Exception as e:
            continue  # Skip this image

    return similar_logos
