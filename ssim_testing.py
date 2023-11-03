from PIL import Image
from skimage import io, color, img_as_ubyte, transform
from skimage.metrics import structural_similarity as ssim
import os

image1Path = os.path.join('MainAlgorithm', 'Database_PNGs-1000', 'abplive.com.ico.png')
image2Path = os.path.join('MainAlgorithm', 'Database_PNGs-1000', 'adobe.io.ico.png')

# Load the images using PIL (Pillow)
image1 = Image.open(image1Path)
image2 = Image.open(image2Path)

# Convert images to grayscale
image1 = image1.convert('L')
image2 = image2.convert('L')

# Resize images to the same dimensions
width, height = 100, 100  # Set the desired dimensions
image1 = image1.resize((width, height))
image2 = image2.resize((width, height))

# Convert PIL images to NumPy arrays
image1 = img_as_ubyte(image1)
image2 = img_as_ubyte(image2)

# Calculate SSIM between the two images
similarity = ssim(image1, image2, data_range=image2.max() - image2.min())

print("SSIM:", similarity)