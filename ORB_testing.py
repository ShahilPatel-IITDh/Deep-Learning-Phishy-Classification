import cv2
import numpy as np

# Load the two images you want to compare
image1 = cv2.imread('image1.jpg', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('image2.jpg', cv2.IMREAD_GRAYSCALE)

# Initialize the ORB detector
orb = cv2.ORB_create()

# Find the key points and descriptors for both images
keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
keypoints2, descriptors2 = orb.detectAndCompute(image2, None)

# Create a BFMatcher (Brute-Force Matcher) object with Hamming distance
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match the descriptors
matches = bf.match(descriptors1, descriptors2)

# Sort the matches by their distances (lower distance means a better match)
matches = sorted(matches, key=lambda x: x.distance)

# Calculate the structural similarity score
ssim_score = len(matches)

print(f"Structural Similarity Score: {ssim_score}")
