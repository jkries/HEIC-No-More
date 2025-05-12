import os
from PIL import Image
from PIL import ImageTk
import pillow_heif
pillow_heif.register_heif_opener()
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import subprocess
import sys
import webbrowser

selected_directory = None
converted_directory = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def convert_images(format):
    global total_converted
    total_converted = 0
    heic_files = [f for f in os.listdir(selected_directory) if f.lower().endswith('.heic')]
    total_files = len(heic_files)

    for index, filename in enumerate(heic_files, start=1):
        heic_file_path = os.path.join(selected_directory, filename)
        converted_file_name = os.path.splitext(filename)[0] + f'.{format.lower()}'
        converted_file_path = os.path.join(converted_directory, converted_file_name)

        with Image.open(heic_file_path) as img:
            img.convert("RGB").save(converted_file_path, format.upper())
            total_converted += 1
            status_label.config(text=f"Converting {index} of {total_files}")

    status_label.config(text=f"Conversion complete: {total_converted} files converted.")
    done_label.pack()  # Show the done label
    if os.path.exists(converted_directory):
        os.startfile(converted_directory)

def start_conversion(format):
    if not selected_directory:
        messagebox.showerror("Error", "Please select a directory first.")
        return

    global converted_directory
    converted_directory = os.path.join(selected_directory, "converted")
    if not os.path.exists(converted_directory):
        os.makedirs(converted_directory)

    conversion_thread = threading.Thread(target=convert_images, args=(format,))
    conversion_thread.start()

def browse_directory():
    global selected_directory, converted_directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        convert_jpg_button.config(state=tk.NORMAL)
        convert_png_button.config(state=tk.NORMAL)
        status_label.config(text=f"Selected directory: {selected_directory}")
        converted_directory = os.path.join(selected_directory, "converted")
    else:
        convert_jpg_button.config(state=tk.DISABLED)
        convert_png_button.config(state=tk.DISABLED)
        status_label.config(text="Select a directory to start.")

def open_github(event):
    webbrowser.open_new("https://github.com/jkries")

# Initialize the main window
root = tk.Tk()
root.title("HEIC-No-More Image Converter")
root.geometry("600x600")  # Set window size to 500px wide, 500px tall
root.iconbitmap(resource_path(os.path.join('icons', 'favicon.ico')))

apple_icon_path = resource_path(os.path.join('icons', 'apple-touch-icon.png'))
apple_img = Image.open(apple_icon_path)
apple_photo = ImageTk.PhotoImage(apple_img)
image_label = tk.Label(root, image=apple_photo)
image_label.image = apple_photo  # Keep a reference!
image_label.pack(pady=(5, 5))

header_label = tk.Label(root, text="How to use this tool:", font=("TkDefaultFont", 12, "bold"))
header_label.pack(pady=(10, 0))

instructions_label = tk.Label(
    root,
    text="Step 1: Use the browse button to find a folder with HEIC image files in it\nStep 2: Choose to convert to JPG or PNG\nStep 3: Wait for the conversion process to run",
    wraplength=480,
    justify="left"
)
instructions_label.pack(pady=(5, 5))

# Create and place widgets
browse_button = tk.Button(root, text="Browse for an image folder", command=browse_directory)
browse_button.pack(pady=10)

convert_jpg_button = tk.Button(root, text="Convert to JPG", state=tk.DISABLED, command=lambda: start_conversion('JPEG'))
convert_jpg_button.pack(pady=5)

convert_png_button = tk.Button(root, text="Convert to PNG", state=tk.DISABLED, command=lambda: start_conversion('PNG'))
convert_png_button.pack(pady=5)

status_label = tk.Label(root, text="Select a directory to start.")
status_label.pack(pady=20)

done_label = tk.Label(root, text="You may now close this window", fg="green")
done_label.pack()
done_label.pack_forget()  # Hide initially

disclaimer_label = tk.Label(
    root,
    text='This tool is provided "as is" without warranty of any kind. Use at your own risk.',
    fg='gray',
    font=("TkDefaultFont", 8),
    wraplength=480,
    justify="center"
)

link_label = tk.Label(
    root,
    text="Jay Made This",
    fg="blue",
    cursor="hand2",
    font=("TkDefaultFont", 9, "underline")
)
disclaimer_label.pack(side="bottom", pady=(0, 10))
link_label.pack(side="bottom", pady=(0, 5))
link_label.bind("<Button-1>", open_github)

# Start the Tkinter event loop
root.mainloop()
