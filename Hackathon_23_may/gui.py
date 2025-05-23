import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import logic

class ImageTransformerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Transformer Tool")
        self.root.geometry("900x600")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.original_img = None
        self.processed_img = None

        # Main frame
        main_frame = ttk.Frame(root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Canvas with clickable placeholder
        self.canvas = tk.Canvas(main_frame, bg='gray')
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Button-1>", lambda e: self.upload_image())
        self.placeholder_text_id = self.canvas.create_text(
            300, 200,
            text="Upload an image here",
            fill="white",
            font=("Helvetica", 16, "bold"),
            anchor="center"
        )

        # Controls Panel
        control_panel = ttk.Frame(main_frame)
        control_panel.grid(row=0, column=1, sticky="n")

        ttk.Button(control_panel, text="Upload Image", command=self.upload_image).pack(fill="x", pady=5)

        self.transform_var = tk.StringVar()
        self.transform_menu = ttk.Combobox(control_panel, textvariable=self.transform_var, state="readonly")
        self.transform_menu['values'] = [
            "Grayscale", "Gaussian Blur", "Median Blur", "Sobel Edge",
            "Canny Edge", "Threshold Binary", "Rotate", "Resize",
            "Erosion", "Dilation", "Brightness", "Contrast",
            "Flip Horizontal", "Flip Vertical"
        ]
        self.transform_menu.set("Select Transformation")
        self.transform_menu.pack(fill="x", pady=5)
        self.transform_menu.bind("<<ComboboxSelected>>", lambda e: self.on_transform_change(self.transform_var.get()))

        self.controls_frame = ttk.Frame(control_panel)
        self.controls_frame.pack(fill="x", pady=5)

        button_frame = ttk.Frame(control_panel)
        button_frame.pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Apply", command=self.apply_transform).pack(side="left", expand=True, padx=2)
        ttk.Button(button_frame, text="Reset", command=self.reset_image).pack(side="left", expand=True, padx=2)
        ttk.Button(button_frame, text="Save", command=self.save_image).pack(side="left", expand=True, padx=2)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w")
        self.status_label.grid(row=1, column=0, sticky="ew")
        self.set_status("Ready")

        self.param_sliders = {}

    def set_status(self, text):
        self.status_var.set(text)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return
        img = cv2.imread(file_path)
        if img is None:
            messagebox.showerror("Error", "Failed to load image.")
            return
        self.original_img = img
        self.processed_img = img.copy()
        self.show_image(self.processed_img)
        self.transform_var.set("Select Transformation")
        self.clear_controls()
        self.set_status(f"Loaded {file_path}")

    def show_image(self, img_cv):
        self.canvas.delete("all")  # Clear canvas

        if len(img_cv.shape) == 2:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_GRAY2RGB)
        else:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

        h, w = img_cv.shape[:2]
        scale = min(600/w, 400/h)
        img_resized = cv2.resize(img_cv, (int(w*scale), int(h*scale)))

        img_pil = Image.fromarray(img_resized)
        self.tk_img = ImageTk.PhotoImage(img_pil)

        self.canvas.config(width=img_resized.shape[1], height=img_resized.shape[0])
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

    def on_transform_change(self, selection):
        self.clear_controls()
        if self.original_img is None:
            return

        if selection in ("Gaussian Blur", "Median Blur", "Erosion", "Dilation"):
            self.add_slider("Kernel Size", 1, 31, 5, self.apply_transform, odd_only=True)
        elif selection == "Canny Edge":
            self.add_slider("Low Threshold", 0, 255, 100, self.apply_transform)
            self.add_slider("High Threshold", 0, 255, 200, self.apply_transform)
        elif selection == "Threshold Binary":
            self.add_slider("Threshold", 0, 255, 127, self.apply_transform)
        elif selection == "Rotate":
            self.add_slider("Angle", -180, 180, 0, self.apply_transform)
        elif selection == "Resize":
            self.add_slider("Scale %", 10, 300, 100, self.apply_transform)
        elif selection == "Brightness":
            self.add_slider("Brightness", -100, 100, 0, self.apply_transform)
        elif selection == "Contrast":
            self.add_slider("Contrast (x)", 10, 300, 120, self.apply_transform)
        else:
            self.apply_transform()

    def add_slider(self, name, min_val, max_val, init_val, command, odd_only=False):
        frame = tk.Frame(self.controls_frame)
        frame.pack(pady=2)
        label = tk.Label(frame, text=name)
        label.pack(side=tk.LEFT)
        
        slider = tk.Scale(frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                        command=lambda v: self.apply_transform())  # Fix here
        slider.set(init_val)
        slider.pack(side=tk.LEFT)
        
        self.param_sliders[name] = (slider, odd_only)


    def get_slider_value(self, name):
        slider, odd_only = self.param_sliders.get(name, (None, False))
        if slider:
            val = int(slider.get())
            if odd_only and val % 2 == 0:
                val += 1
            return val
        return None

    def apply_transform(self):
        if self.original_img is None:
            return
        selection = self.transform_var.get()
        img = self.original_img.copy()

        if selection == "Grayscale":
            img = logic.to_grayscale(img)
        elif selection == "Gaussian Blur":
            img = logic.gaussian_blur(img, self.get_slider_value("Kernel Size"))
        elif selection == "Median Blur":
            img = logic.median_blur(img, self.get_slider_value("Kernel Size"))
        elif selection == "Sobel Edge":
            img = logic.sobel_edge(img)
        elif selection == "Canny Edge":
            img = logic.canny_edge(img, self.get_slider_value("Low Threshold"), self.get_slider_value("High Threshold"))
        elif selection == "Threshold Binary":
            img = logic.threshold_binary(img, self.get_slider_value("Threshold"))
        elif selection == "Rotate":
            img = logic.rotate_image(img, self.get_slider_value("Angle"))
        elif selection == "Resize":
            scale = self.get_slider_value("Scale %") / 100.0
            img = logic.resize_image(img, scale)
        elif selection == "Erosion":
            img = logic.erosion(img, self.get_slider_value("Kernel Size"))
        elif selection == "Dilation":
            img = logic.dilation(img, self.get_slider_value("Kernel Size"))
        elif selection == "Brightness":
            img = logic.adjust_brightness(img, self.get_slider_value("Brightness"))
        elif selection == "Contrast":
            img = logic.adjust_contrast(img, self.get_slider_value("Contrast (x)") / 100)
        elif selection == "Flip Horizontal":
            img = logic.flip_image(img, "horizontal")
        elif selection == "Flip Vertical":
            img = logic.flip_image(img, "vertical")

        self.processed_img = img
        self.show_image(img)
        self.set_status(f"Applied {selection}")

    def clear_controls(self):
        for widget in self.controls_frame.winfo_children():
            widget.destroy()
        self.param_sliders.clear()

    def reset_image(self):
        if self.original_img is None:
            return
        self.processed_img = self.original_img.copy()
        self.show_image(self.processed_img)
        self.clear_controls()
        self.set_status("Image reset")

    def save_image(self):
        if self.processed_img is None:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if not file_path:
            return
        img_to_save = self.processed_img
        if len(img_to_save.shape) == 2:
            img_to_save = cv2.cvtColor(img_to_save, cv2.COLOR_GRAY2BGR)
        cv2.imwrite(file_path, img_to_save)
        self.set_status(f"Saved to {file_path}")
