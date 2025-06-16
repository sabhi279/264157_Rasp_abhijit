import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np
from ocr_utils import extract_plate_text
from mqtt_client import publish_plate
from datetime import datetime
import base64
from io import BytesIO

class PlateDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Plate Detection")
        self.root.geometry("320x640")
        self.root.resizable(False, False)

        self.image_path = None
        self.cv2_image = None
        self.display_image = None

        self.create_scrollable_ui()

    def create_scrollable_ui(self):
        # Canvas and scrollbar to make it scrollable
        self.canvas = tk.Canvas(self.root, width=320, height=640)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.setup_ui(self.scrollable_frame)

    def setup_ui(self, frame):
        # Upload button
        tk.Button(frame, text="Upload Image", command=self.load_image).pack(pady=10)

        # Image display area
        self.image_label = tk.Label(frame)
        self.image_label.pack()

        # Brightness slider
        self.brightness = tk.Scale(frame, from_=0.5, to=2.0, resolution=0.1,
                                   label="Brightness", orient=tk.HORIZONTAL, command=self.update_image)
        self.brightness.set(1.0)
        self.brightness.pack()

        # Contrast slider
        self.contrast = tk.Scale(frame, from_=0.5, to=2.0, resolution=0.1,
                                 label="Contrast", orient=tk.HORIZONTAL, command=self.update_image)
        self.contrast.set(1.0)
        self.contrast.pack()

        # Detect button
        tk.Button(frame, text="Detect Plate", command=self.detect_plate).pack(pady=10)

        # Result label
        self.result_label = tk.Label(frame, text="Detected Plate: ")
        self.result_label.pack(pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image_path = file_path
            self.cv2_image = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
            self.update_image()

    def update_image(self, event=None):
        if self.cv2_image is None:
            return

        img = Image.fromarray(self.cv2_image)

        # Apply brightness and contrast
        img = ImageEnhance.Brightness(img).enhance(self.brightness.get())
        img = ImageEnhance.Contrast(img).enhance(self.contrast.get())

        self.display_image = img
        img_resized = img.resize((280, 200))  # Fit image inside scroll view
        photo = ImageTk.PhotoImage(img_resized)

        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def detect_plate(self):
        if self.display_image is None:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        img_np = np.array(self.display_image)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        plates = extract_plate_text(img_bgr)

        if plates:
            text, conf = plates[0]
            self.result_label.config(text=f"Detected Plate: {text} (Confidence: {conf:.2f})")
        else:
            self.result_label.config(text="No valid plate detected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlateDetectionApp(root)
    root.mainloop()
