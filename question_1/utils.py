#utils
import cv2
from PIL import Image, ImageTk

def load_image(file_path):
    """
    Loads an image from the given file path using OpenCV and converts it from BGR to RGB format.
    
    Args:
        file_path (str): Path to the image file to be loaded.
        
    Returns:
        numpy.ndarray: The image array in RGB color space.
    
    Raises:
        FileNotFoundError: If the image cannot be loaded (file does not exist or is invalid).
    """
    # Read the image using OpenCV (which loads images in BGR format by default)
    img = cv2.imread(file_path)
    if img is None:
        # Raise error if the image failed to load
        raise FileNotFoundError(f"Unable to load image at: {file_path}")
    
    # Convert the image from BGR to RGB format (required for correct color display in PIL/Tkinter)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def convert_to_tk(image_array):
    """
    Converts a NumPy image array (RGB) into a PhotoImage object compatible with Tkinter widgets.
    
    Args:
        image_array (numpy.ndarray): The image data in RGB format.
        
    Returns:
        ImageTk.PhotoImage: Tkinter-compatible image object for displaying on GUI widgets.
    """
    # Convert NumPy array to PIL Image object
    image = Image.fromarray(image_array)
    
    # Convert PIL Image to Tkinter PhotoImage for use in GUI
    return ImageTk.PhotoImage(image)

def save_image(image_array, path):
    """
    Saves an RGB image array to disk as an image file.
    
    Args:
        image_array (numpy.ndarray): The image data in RGB format.
        path (str): The destination file path where the image should be saved.
        
    Returns:
        None
    """
    # Convert the RGB image to BGR format for OpenCV before saving
    bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    
    # Write the image to disk at the specified path
    cv2.imwrite(path, bgr_image)
