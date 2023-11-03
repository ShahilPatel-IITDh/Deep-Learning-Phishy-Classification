import cv2
import os

def ORB(img1, img2):
    image1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)

    if image1 is None or image2 is None:
        print("Error: Could not load images.")
        return 0

    orb = cv2.ORB_create(nfeatures=1000, scoreType=cv2.ORB_FAST_SCORE)
    
    keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image2, None)

    if keypoints1 and keypoints2:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)

        # Calculate the normalized Hamming distance
        max_distance = max([match.distance for match in matches])
        similarity_score = 1 - (sum(match.distance / max_distance for match in matches) / len(matches))

        result = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:10], None)

        # Display the result (uncomment these lines if you want to visualize)
        # cv2.imshow("Matching Result", result)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return similarity_score
    else:
        print("Error: No keypoints found in one of the images.")
        return 0

if __name__ == "__main__":
    image1Path = os.path.join('MainAlgorithm', 'Database_PNGs-1000','3bmeteo.com.ico.png')
    image2Path = os.path.join('MainAlgorithm', 'Database_PNGs-1000','3bmeteo.com.ico.png')
    orb_score = ORB(image1Path, image2Path)
    
    if orb_score is not None:
        print(f"ORB Similarity Score: {orb_score:.4f}")
    else:
        print("Unable to calculate similarity score.")