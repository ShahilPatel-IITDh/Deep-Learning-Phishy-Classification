import tensorflow as tf
import numpy as np
from scipy.spatial.distance import cosine
import os

# Load the pre-trained VGG16 model
model = tf.keras.applications.VGG16(weights='imagenet', include_top=False)

# Function to preprocess and extract features from an image
def extract_features(image_path, model):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.vgg16.preprocess_input(img)
    features = model.predict(img)
    return features.flatten()  # Flatten the feature tensor


# Extract features from the images
def detect_logo_similarity(suscpiciousLogo, logoDatabase):
    
    similarLogos = {}

    features1 = extract_features(suscpiciousLogo, model)

    for logo in logoDatabase:
        features2 = extract_features(logo, model)

        # Calculate the cosine similarity between the feature vectors
        similarity = 1 - cosine(features1, features2)

        # Set a similarity threshold (e.g., 0.8)
        threshold = 0.8

        # Check if the similarity is above the threshold
        if similarity >= threshold:
            # os.path.basename() returns the filename from a path
            similarLogos[os.path.basename(logo)] = similarity * 100
    
    return similarLogos