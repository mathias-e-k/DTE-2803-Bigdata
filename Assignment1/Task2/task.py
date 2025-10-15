import pydicom
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Harnverhalt is german for 'Urinary retention'


number = 1

def increase():
    global number
    number += 1
    update_dicom_image()
    print(f"Current number: {number:04d}")  # Print the number to the console for debugging

def decrease():
    global number
    number = max(1, number - 1)  # Prevent negative numbers
    update_dicom_image()
    print(f"Current number: {number:04d}")  # Print the number to the console for debugging

def set_number():
    global number
    try:
        new_value = int(entry_box.get())
        if new_value < 1:
            raise ValueError("Number must be non-negative.")
        number = new_value
        update_dicom_image()
        print(f"Current number: {number:04d}")  # Print the number to the console for debugging
    except ValueError:
        error_label.config(text="Please enter a valid non-negative integer.")
    else:
        error_label.config(text="")

def load_dicom_image(file_path):
    dicom_data = pydicom.dcmread(file_path)
    pixel_array = dicom_data.pixel_array
    
    # Normalize the pixel values to fit in the range [0, 255]
    pixel_array_normalized = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX)
    
    # Convert to 8-bit unsigned integers
    pixel_array_uint8 = pixel_array_normalized.astype(np.uint8)
    
    # Convert to a PIL Image
    image = Image.fromarray(pixel_array_uint8)
    
    # Convert the PIL Image to a format Tkinter can use
    tk_image = ImageTk.PhotoImage(image)

    return tk_image

def reconstruct(img):
    # Morphological operation Close (Dilation and Erosion)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morphed_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    # K-means clustering
    k = 5  # Number of clusters
    pixels = morphed_img.reshape(-1, 1)
    kmeans = cv2.kmeans(np.float32(pixels), k, None,
                    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2),
                    attempts = 10,
                    flags = cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(kmeans[2])
    segmented_image = centers[kmeans[1].flatten()]
    segmented_image = segmented_image.reshape(morphed_img.shape)

    # # PCA
    # pca = PCA(n_components=1)  # Adjust components as needed
    # flattened = segmented_image.flatten()
    # reduced = pca.fit_transform(flattened.reshape(1, -1))
    # reconstructed = pca.inverse_transform(reduced).reshape(segmented_image.shape)

    return segmented_image


def load_dicom_image_test(file_path):
    dicom_data = pydicom.dcmread(file_path)
    pixel_array = dicom_data.pixel_array
    
    # Normalize the pixel values to fit in the range [0, 255]
    pixel_array_normalized = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX)
    
    # Convert to 8-bit unsigned integers
    pixel_array_uint8 = pixel_array_normalized.astype(np.uint8)

    image_modified = reconstruct(pixel_array_uint8)

    # Convert to a PIL Image
    image = Image.fromarray(pixel_array_uint8)
    image_modified = Image.fromarray(image_modified)

    # Convert the PIL Image to a format Tkinter can use
    tk_image = ImageTk.PhotoImage(image)
    tk_image_modified = ImageTk.PhotoImage(image_modified)

    return tk_image, tk_image_modified

def update_dicom_image():
    global number
    file_path = f"1/Harnverhalt/{number:04d}.dcm"
    print(file_path)
    tk_image, tk_image_modified = load_dicom_image_test(file_path)
    label_original.config(image=tk_image)
    label_original.image = tk_image

    label_modified.config(image=tk_image_modified)
    label_modified.image = tk_image_modified


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Harnverhalt")
    file_path = f"1/Harnverhalt/{number:04d}.dcm"
    print(file_path)
    tk_image, tk_image_modified = load_dicom_image_test(file_path)


    # Images
    image_frame = tk.Frame(root)
    image_frame.pack(pady=10)
    # Original image
    label_original = tk.Label(image_frame, image=tk_image)
    label_original.pack(side="left", padx=10)
    label_modified = tk.Label(image_frame, image=tk_image_modified)
    label_modified.pack(side="left", padx=10)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    increase_button = tk.Button(button_frame, text="Increase", command=increase, font=("Helvetica", 14))
    increase_button.pack(side="left", padx=10)
    decrease_button = tk.Button(button_frame, text="Decrease", command=decrease, font=("Helvetica", 14))
    decrease_button.pack(side="left", padx=10)

    # Entry box to jump to any number
    entry_frame = tk.Frame(root)
    entry_frame.pack(pady=10)
    entry_label = tk.Label(entry_frame, text="Jump to:", font=("Helvetica", 14))
    entry_label.pack(side="left", padx=5)
    entry_box = tk.Entry(entry_frame, font=("Helvetica", 14), width=10)
    entry_box.pack(side="left", padx=5)
    set_button = tk.Button(entry_frame, text="Set", command=set_number, font=("Helvetica", 14))
    set_button.pack(side="left", padx=5)

    error_label = tk.Label(root, text="", font=("Helvetica", 12), fg="red")
    error_label.pack(pady=5)

    root.mainloop()



