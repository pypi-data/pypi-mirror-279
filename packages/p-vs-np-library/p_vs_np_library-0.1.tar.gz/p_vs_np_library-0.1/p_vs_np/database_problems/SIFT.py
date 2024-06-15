#SIFT

import cv2

def sift_feature_extraction(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create a SIFT object
    sift = cv2.xfeatures2d.SIFT_create()

    # Detect and compute keypoints and descriptors
    keypoints, descriptors = sift.detectAndCompute(gray, None)

    # Draw the keypoints on the image
    image_with_keypoints = cv2.drawKeypoints(image, keypoints, None)

    # Display the image with keypoints
    cv2.imshow("SIFT Features", image_with_keypoints)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = "image.jpg"  # Path to the image file

sift_feature_extraction(image_path)

