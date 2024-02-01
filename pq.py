import tkinter as tk
import face_recognition
import shutil
import glob
import os
from tkinter import filedialog


def process_inputs():
    # Load the known image and encode the face
    known_img_address = entry1.get()
    known_image = face_recognition.load_image_file(known_img_address)
    known_encoding = face_recognition.face_encodings(known_image)[0]

    # Set the source and destination folders
    source_address = entry2.get()
    destination_address = entry3.get()

    # Get a list of all the file names of jpg files in the source folder
    jpg_files = glob.glob(source_address + '/*.jpg')

    # specify the name and path of the folder you want to create
    new_folder = "destination\\" + destination_address

    # use the os module to create the folder
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print(f"Folder '{new_folder}' created successfully!")
    else:
        print(f"Folder '{new_folder}' already exists.")

    # Loop through each jpg file in the source folder
    for jpg_file in jpg_files:
        # Load the image and find all the face locations and encodings
        image = face_recognition.load_image_file(jpg_file)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # Loop through each face in the image and compare to the known encoding
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            match = face_recognition.compare_faces([known_encoding], face_encoding)[0]

            # If a match is found, save the image and exit the loop
            if match:
                shutil.copy(jpg_file, new_folder)
                break

    print("Done processing images.")

def select_source_location():
    source_location = filedialog.askdirectory()
    entry2.delete(0, tk.END)
    entry2.insert(0, source_location)

def select_destination_location():
    destination_location = filedialog.askdirectory()
    entry3.delete(0, tk.END)
    entry3.insert(0, destination_location)

# Create the root window
root = tk.Tk()
root.title("Picture Filter")

# Use a custom font for the labels and entries
font = ("Helvetica", 12)

# Add padding and spacing between the elements
label1 = tk.Label(root, text="Known Face:", font=font, padx=10, pady=10)
label1.grid(row=0, column=0)

entry1 = tk.Entry(root, font=font)
entry1.grid(row=0, column=1)

label2 = tk.Label(root, text="Source Location:", font=font, padx=10, pady=10)
label2.grid(row=1, column=0)

entry2 = tk.Entry(root, font=font)
entry2.grid(row=1, column=1)

# Add a button to open a file dialog box for selecting the source location
button2 = tk.Button(root, text="Browse", command=select_source_location)
button2.grid(row=1, column=2)

label3 = tk.Label(root, text="Destination Location:", font=font, padx=10, pady=10)
label3.grid(row=2, column=0)

entry3 = tk.Entry(root, font=font)
entry3.grid(row=2, column=1)

# Add a button to open a file dialog box for selecting the destination location
# button3 = tk.Button(root, text="Browse", command=select_destination_location)
# button3.grid(row=2, column=2)

button = tk.Button(root, text="Submit", font=font, command=process_inputs)
button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Add an image or icon to the application title
icon = tk.PhotoImage(file="856981.png")
root.iconphoto(True, icon)

# Add a status bar to display messages to the user
status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.grid(row=4, column=0, columnspan=3, sticky=tk.W+tk.E)

root.mainloop()
