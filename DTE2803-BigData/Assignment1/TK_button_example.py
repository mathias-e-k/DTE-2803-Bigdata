import tkinter as tk
# Function to update the label with a formatted number
def update_label(value):
    number_label.config(text=f"{value:04d}")
# Function to increase the number
def increase():
    current_value = int(number_label["text"])
    update_label(current_value + 1)
# Function to decrease the number
def decrease():
    current_value = int(number_label["text"])
    update_label(max(0, current_value - 1))  # Prevent negative numbers
# Function to set the number from the entry box
def set_number():
    try:
        new_value = int(entry_box.get())
        if new_value < 0:
            raise ValueError("Number must be non-negative.")
        update_label(new_value)
    except ValueError:
        # Show an error message if the input is invalid
        error_label.config(text="Please enter a valid non-negative integer.")
    else:
        # Clear the error message if the input is valid
        error_label.config(text="")
# Create the main application window
root = tk.Tk()
root.title("Number Counter")
# Create a label to display the number
number_label = tk.Label(root, text="0000", font=("Helvetica", 48))
number_label.pack(pady=20)
# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
# Create the "Increase" button
increase_button = tk.Button(button_frame, text="Increase", command=increase, font=("Helvetica", 14))
increase_button.pack(side="left", padx=10)
# Create the "Decrease" button
decrease_button = tk.Button(button_frame, text="Decrease", command=decrease, font=("Helvetica", 14))
decrease_button.pack(side="left", padx=10)
# Create an entry box to input a number
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)
entry_label = tk.Label(entry_frame, text="Jump to:", font=("Helvetica", 14))
entry_label.pack(side="left", padx=5)
entry_box = tk.Entry(entry_frame, font=("Helvetica", 14), width=10)
entry_box.pack(side="left", padx=5)
set_button = tk.Button(entry_frame, text="Set", command=set_number, font=("Helvetica", 14))
set_button.pack(side="left", padx=5)
# Create a label to display error messages
error_label = tk.Label(root, text="", font=("Helvetica", 12), fg="red")
error_label.pack(pady=5)
# Run the application
root.mainloop()