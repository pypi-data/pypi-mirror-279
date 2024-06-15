#SIFT


    # Load the image

    # Check if the image was loaded

    # Convert the image to grayscale

    # Create a SIFT object

    # Detect and compute keypoints and descriptors

    # Draw the keypoints on the image

    # Display the image with keypoints


# Example usage



if __name__ == '__main__':
    import cv2
    def sift_feature_extraction(image_path):
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to open image file {image_path}")
            return
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(gray, None)
        image_with_keypoints = cv2.drawKeypoints(image, keypoints, None)
        cv2.imshow("SIFT Features", image_with_keypoints)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    image_path = "image.jpg"  # Path to the image file
    sift_feature_extraction(image_path)
