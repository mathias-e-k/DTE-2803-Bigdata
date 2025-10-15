import cv2
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pydicom
# Load the grayscale image
# image = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)
dicom_data = pydicom.dcmread("1/Harnverhalt/0001.dcm")
pixel_array = dicom_data.pixel_array
    
    # Normalize the pixel values to fit in the range [0, 255]
image = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX)
    
# Add synthetic noise to the image for demonstration
noisy_image = image + np.random.normal(0, 25, image.shape).astype(np.uint8)  # Add Gaussian noise
noisy_image = np.clip(noisy_image, 0, 255)  # Ensure pixel values are in range [0, 255]
# Flatten the image into a 2D array (rows = pixels, columns = features)
# Treat each row of the image as a "sample" (e.g., a row of pixels)
image_flattened = image.astype(np.float32)
# Apply PCA
pca = PCA(n_components=50)  # Retain only the top 50 principal components
image_pca = pca.fit_transform(image_flattened)  # Transform the noisy image
image_reconstructed = pca.inverse_transform(image_pca)  # Reconstruct the image from PCA
# Reshape the reconstructed image back to its original shape
denoised_image = image_reconstructed.astype(np.uint8)
# Visualize the original, noisy, and denoised images
plt.figure(figsize=(15, 5))
# Original image
plt.subplot(1, 3, 1)
plt.title("Original Image")
plt.imshow(image, cmap='gray')
plt.axis('off')
# Noisy image
plt.subplot(1, 3, 2)
plt.title("Noisy Image")
plt.imshow(noisy_image, cmap='gray')
plt.axis('off')
# Denoised image
plt.subplot(1, 3, 3)
plt.title("Denoised Image (PCA)")
plt.imshow(denoised_image, cmap='gray')
plt.axis('off')
plt.show()