
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
from PIL import Image, ImageTk
import os

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        self.root.geometry("1000x650")

        # Initialize image variables
        self.original_image = None        # Original loaded image (BGR)
        self.display_image = None         # Image currently displayed (RGB or other modes)
        self.cropped_image = None         # Cropped portion of the image
        self.resized_image = None         # Resized cropped image for saving/preview
        self.tk_resized = None            # Tkinter PhotoImage for preview label
        self.image_path = None            # Path of the loaded image
        self.color_mode = 'RGB'           # Current color mode selected

        # Variables to track cropping rectangle coordinates
        self.start_x = self.start_y = self.end_x = self.end_y = None
        self.rect_id = None               # Canvas rectangle ID

        # Maximum display dimensions for loaded images
        self.MAX_WIDTH, self.MAX_HEIGHT = 700, 600
        self.is_dark = False              # Dark mode flag

        # Setup UI components and bind shortcuts
        self.setup_ui()
        self.bind_shortcuts()

    def setup_ui(self):
        # Create a canvas to display the image
        self.canvas = tk.Canvas(self.root, bg="gray", width=self.MAX_WIDTH, height=self.MAX_HEIGHT)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind mouse events for cropping: click, drag, release
        self.canvas.bind("<Button-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.finish_crop)

        # Control panel on the right side
        self.control_frame = tk.Frame(self.root, width=300)
        self.control_frame.pack(side="right", fill="y", padx=10)

        # Buttons for loading, saving, and resetting the image
        ttk.Button(self.control_frame, text="Load Image", command=self.load_image).pack(pady=8)
        ttk.Button(self.control_frame, text="Save Cropped Image", command=self.save_image).pack(pady=8)
        ttk.Button(self.control_frame, text="Reset Image", command=self.reset_image).pack(pady=8)

        # Slider for resizing the cropped image (10% to 200%)
        ttk.Label(self.control_frame, text="Resize Cropped Image").pack(pady=5)
        self.resize_slider = ttk.Scale(self.control_frame, from_=10, to=200, orient='horizontal', command=self.resize_image)
        self.resize_slider.set(100)  # Default to 100% scale
        self.resize_slider.pack(pady=5)

        # Radio buttons for selecting color mode (RGB, HSV, Grayscale)
        ttk.Label(self.control_frame, text="Color Mode").pack(pady=5)
        self.color_var = tk.StringVar(value='RGB')
        for mode in ['RGB', 'HSV', 'Grayscale']:
            ttk.Radiobutton(self.control_frame, text=mode, value=mode, variable=self.color_var, command=self.apply_color_mode).pack(anchor="w")

        # Checkbox to toggle dark mode
        self.dark_var = tk.BooleanVar()
        ttk.Checkbutton(self.control_frame, text="Dark Mode", variable=self.dark_var, command=self.toggle_dark_mode).pack(pady=10)

        # Label to preview the cropped/resized image
        ttk.Label(self.control_frame, text="Preview").pack()
        self.preview_label = tk.Label(self.control_frame)
        self.preview_label.pack(pady=5)

        # Label to show image info like format and size
        self.info_label = ttk.Label(self.control_frame, text="", foreground="blue")
        self.info_label.pack(pady=5)

        # Label to show status messages
        self.status = ttk.Label(self.control_frame, text="", foreground="green")
        self.status.pack(pady=5)

    def bind_shortcuts(self):
        # Bind Ctrl+O to load image, Ctrl+S to save cropped image
        self.root.bind('<Control-o>', lambda e: self.load_image())
        self.root.bind('<Control-s>', lambda e: self.save_image())

    def load_image(self):
        # Open file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if not file_path:
            return

        # Load image using OpenCV (BGR format)
        img = cv2.imread(file_path)
        if img is None:
            messagebox.showerror("Error", "Unable to load image.")
            return

        # Resize image if larger than max allowed display size
        h, w = img.shape[:2]
        if w > self.MAX_WIDTH or h > self.MAX_HEIGHT:
            scale = min(self.MAX_WIDTH / w, self.MAX_HEIGHT / h)
            img = cv2.resize(img, (int(w * scale), int(h * scale)))

        # Store original and display images
        self.image_path = file_path
        self.original_image = img.copy()
        self.display_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for display

        # Apply current color mode and show image on canvas
        self.apply_color_mode()
        self.show_image(self.display_image)

        # Show image format and size info
        img_format = os.path.splitext(file_path)[-1].upper().replace('.', '')
        self.info_label.config(text=f"Format: {img_format}, Size: {self.display_image.shape[1]}x{self.display_image.shape[0]}")
        self.status.config(text="Image loaded.")

    def reset_image(self):
        # Reset the image view and clear cropping/resize info
        if self.original_image is None:
            return
        self.display_image = cv2.cvtColor(self.original_image.copy(), cv2.COLOR_BGR2RGB)
        self.apply_color_mode()
        self.cropped_image = None
        self.resized_image = None
        self.show_image(self.display_image)
        self.preview_label.config(image='')
        self.status.config(text="Image reset.")

    def apply_color_mode(self):
        # Apply the selected color mode to the original image
        if self.original_image is None:
            return

        img = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        mode = self.color_var.get()

        if mode == 'HSV':
            img = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)
        elif mode == 'Grayscale':
            img = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        elif mode == 'RGB':
            img = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)

        # For grayscale images, convert single channel to 3-channel RGB for displaying on canvas
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        self.display_image = img
        self.show_image(img)

    def toggle_dark_mode(self):
        # Toggle between dark and light modes by changing background and text colors
        self.is_dark = self.dark_var.get()
        color = "#333333" if self.is_dark else "#f0f0f0"
        fg_color = "white" if self.is_dark else "black"
        self.root.configure(bg=color)
        self.control_frame.configure(bg=color)

        # Update all widgets in control frame with appropriate bg and fg colors
        for widget in self.control_frame.winfo_children():
            try:
                widget.configure(background=color, foreground=fg_color)
            except:
                # Some widgets (like ttk) may not support bg/fg configuration; ignore errors
                pass
        self.canvas.configure(bg=color)

    def show_image(self, img):
        # Convert numpy array image to PIL and then to Tkinter PhotoImage to display on canvas
        img_pil = Image.fromarray(img)
        self.tk_img = ImageTk.PhotoImage(img_pil)
        self.canvas.delete("all")  # Clear previous images
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def start_crop(self, event):
        # Begin cropping: store initial click position and create rectangle
        if self.display_image is None:
            return
        self.start_x, self.start_y = event.x, event.y
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def update_crop(self, event):
        # Update cropping rectangle as mouse is dragged
        if self.rect_id:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def finish_crop(self, event):
        # Finish cropping on mouse release: calculate crop box and extract image region
        if self.display_image is None:
            return
        self.end_x, self.end_y = event.x, event.y

        # Normalize coordinates (top-left and bottom-right)
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)

        h, w, _ = self.display_image.shape

        # Clamp coordinates within image bounds
        x1, x2 = max(0, x1), min(w, x2)
        y1, y2 = max(0, y1), min(h, y2)

        # Validate crop area is not empty
        if x2 <= x1 or y2 <= y1:
            self.status.config(text="Invalid crop area!")
            return

        # Crop the selected region from the display image
        self.cropped_image = self.display_image[y1:y2, x1:x2].copy()
        self.resize_slider.set(100)  # Reset resize slider to 100%
        self.status.config(text="Image cropped.")
        self.show_preview(self.cropped_image)

    def resize_image(self, val):
        # Resize the cropped image based on slider value (percentage)
        if self.cropped_image is None:
            return
        scale = float(val) / 100
        h, w = self.cropped_image.shape[:2]
        new_w, new_h = int(w * scale), int(h * scale)
        if new_w == 0 or new_h == 0:
            return

        # Resize the image using OpenCV INTER_AREA for shrinking, INTER_LINEAR for enlarging
        interpolation = cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR
        self.resized_image = cv2.resize(self.cropped_image, (new_w, new_h), interpolation=interpolation)
        self.show_preview(self.resized_image)

    def show_preview(self, img):
        # Show a preview of the (cropped and resized) image in the preview label
        img_pil = Image.fromarray(img)
        self.tk_resized = ImageTk.PhotoImage(img_pil)
        self.preview_label.config(image=self.tk_resized)

    def save_image(self):
        # Save the resized cropped image to a file chosen by the user
        if self.resized_image is None:
            messagebox.showwarning("Warning", "No cropped image to save!")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg")])
        if not save_path:
            return
        # Convert RGB back to BGR for OpenCV save
        img_to_save = cv2.cvtColor(self.resized_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, img_to_save)
        self.status.config(text=f"Image saved: {os.path.basename(save_path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
