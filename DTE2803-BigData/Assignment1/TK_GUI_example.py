import pydicom
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
def load_dicom_image(file_path):
    # Read the DICOM file using pydicom
    dicom_data = pydicom.dcmread(file_path)
    
    # Extract the pixel array
    pixel_array = dicom_data.pixel_array
    
    # Normalize the pixel values to fit in the range [0, 255]
    pixel_array_normalized = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX)
    
    # Convert to 8-bit unsigned integers
    pixel_array_uint8 = pixel_array_normalized.astype(np.uint8)
    
    # Convert to a PIL Image
    image = Image.fromarray(pixel_array_uint8)
    
    return image
def display_dicom_image(file_path):
    # Load the DICOM image
    image = load_dicom_image(file_path)
    
    # Create a Tkinter window
    root = tk.Tk()
    root.title("DICOM Viewer")
    
    # Convert the PIL Image to a format Tkinter can use
    tk_image = ImageTk.PhotoImage(image)
    
    # Create a label to display the image
    label = tk.Label(root, image=tk_image)
    label.pack()
    
    # Run the Tkinter event loop
    root.mainloop()
# Path to the DICOM file
dicom_file_path = "1/Harnverhalt/0001.dcm"
# Display the DICOM image in a Tkinter app
display_dicom_image(dicom_file_path)