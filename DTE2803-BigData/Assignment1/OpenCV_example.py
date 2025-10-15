import pydicom
import cv2
import numpy as np
# Path to the DICOM file
dicom_file_path = "1/Harnverhalt/0001.dcm"
# Read the DICOM file using pydicom
dicom_data = pydicom.dcmread(dicom_file_path)
# Extract the pixel array from the DICOM file
pixel_array = dicom_data.pixel_array
# Normalize the pixel values to fit in the range [0, 255] for display
pixel_array_normalized = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX)
# Convert the pixel array to 8-bit unsigned integers
pixel_array_uint8 = pixel_array_normalized.astype(np.uint8)
# Display the image using OpenCV
cv2.imshow("DICOM Image", pixel_array_uint8)
# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()