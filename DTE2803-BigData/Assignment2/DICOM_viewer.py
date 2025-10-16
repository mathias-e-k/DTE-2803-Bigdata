import pydicom
import cv2
import numpy as np
import tkinter as tk
from tkinter import StringVar
from PIL import Image, ImageTk
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import get_DICOMs
from os import listdir
from os.path import normpath
# DICOM viewer for testing


number = 0

def increase():
    global number
    number += 1
    update_dicom_image()
    # print(f"Current number: {number:04d}")  # Print the number to the console for debugging

def decrease():
    global number
    number = max(0, number - 1)  # Prevent negative numbers
    update_dicom_image()
    # print(f"Current number: {number:04d}")  # Print the number to the console for debugging

def set_number():
    global number
    try:
        new_value = int(entry_box.get())
        if new_value < 0:
            raise ValueError("Number must be non-negative.")
        number = new_value
        update_dicom_image()
        # print(f"Current number: {number:04d}")  # Print the number to the console for debugging
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


def update_dicom_image():
    global number
    file_path = f"{selected_item_var.get()}/{number:04d}.dcm"
    # file_path = f"DTE2803-BigData/Assignment2/DICOMS/DICOM-Paket1/1/20170223_MRA ARTERIEN HALS/MR_Seq._306000_eMIP cor_sag/{number:04d}.dcm"
    # print(file_path)
    tk_image = load_dicom_image(file_path)
    label_original.config(image=tk_image)
    label_original.image = tk_image
    current_label.config(text=f"current file: {number:04d}.dcm")



def on_select(event=None):
    selected_item = selected_item_var.get()
    result_label.config(text=f"files: {listdir(selected_item)[0]} - {listdir(selected_item)[-1]}")
    update_dicom_image()

if __name__ == "__main__":
    sequences = get_DICOMs.get_sequences()

    root = tk.Tk()
    root.title("DICOM viewer")

    selected_item_var = StringVar()
    selected_item_var.set(sequences[1])
    file_path = selected_item_var.get()

    tk_image = load_dicom_image(f"{file_path}/{number:04d}.dcm")



    # Images
    image_frame = tk.Frame(root)
    image_frame.pack(pady=5)
    # Original image
    label_original = tk.Label(image_frame, image=tk_image)
    label_original.pack(side="left", padx=10)

    dropdown = tk.OptionMenu(root, selected_item_var, *sequences, command=on_select)
    dropdown.config(font=("Helvetica", 7))
    dropdown.pack(pady=5)

    selected_item = selected_item_var.get()
    result_label = tk.Label(root, text=f"files: {listdir(selected_item)[0]} - {listdir(selected_item)[-1]}", font=("Helvetica", 14))
    result_label.pack(pady=7)
    current_label = tk.Label(root, text=f"current file: {number:04d}.dcm", font=("Helvetica", 14))
    current_label.pack(pady=7)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    decrease_button = tk.Button(button_frame, text="Prev", command=decrease, font=("Helvetica", 14))
    decrease_button.pack(side="left", padx=10)
    increase_button = tk.Button(button_frame, text="Next", command=increase, font=("Helvetica", 14))
    increase_button.pack(side="left", padx=10)

    # Entry box to jump to any number
    entry_frame = tk.Frame(root)
    entry_frame.pack(pady=5)
    entry_label = tk.Label(entry_frame, text="Jump to:", font=("Helvetica", 14))
    entry_label.pack(side="left", padx=5)
    entry_box = tk.Entry(entry_frame, font=("Helvetica", 14), width=10)
    entry_box.pack(side="left", padx=5)
    set_button = tk.Button(entry_frame, text="Set", command=set_number, font=("Helvetica", 14))
    set_button.pack(side="left", padx=5)

    error_label = tk.Label(root, text="", font=("Helvetica", 12), fg="red")
    error_label.pack(pady=5)





    root.mainloop()



