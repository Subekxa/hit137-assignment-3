# 🖼️ Image Processing App (Tkinter + OpenCV)

This Python desktop application demonstrates core concepts of:

- Object-Oriented Programming (OOP)  
- GUI development using **Tkinter** (Python's standard GUI library)  
- Image processing using **OpenCV** (powerful computer vision library)  

---

## Features

- Load image from your local device via file dialog  
- Draw a rectangle on the image using mouse drag to crop a selected area, with real-time visual feedback  
- Display the cropped image in a preview section alongside the main image  
- Resize the cropped image interactively using a slider, with the preview updating live  
- Save the cropped or resized image back to your device through a save file dialog  
- **Keyboard shortcuts** for faster workflow:  
  - `Ctrl+O`: Open image  
  - `Ctrl+S`: Save image  

---

## Requirements

- Python 3.x installed on your system  
- Install necessary Python packages with pip:

```bash
pip install opencv-python pillow
