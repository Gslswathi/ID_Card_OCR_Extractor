import cv2
import pytesseract
from PIL import Image
import numpy as np

def preprocess_image(image_path: str) -> Image.Image:
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    # Thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Denoising
    denoised = cv2.fastNlMeansDenoising(thresh, h=30)

    # Convert to PIL
    return Image.fromarray(denoised)

def extract_text(image_path: str) -> str:
    image = preprocess_image(image_path)
    return pytesseract.image_to_string(image)