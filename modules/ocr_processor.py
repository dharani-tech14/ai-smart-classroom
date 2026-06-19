import pytesseract
from PIL import Image
import cv2
import numpy as np
import streamlit as st

class OCRProcessor:
    """Extract text from images using OCR."""

    def __init__(self):
        # ⚠️ IMPORTANT: Set Tesseract path (Windows)
        # Change this path based on your system
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def extract_text_from_upload(self, uploaded_file):
        """Extract text directly from Streamlit uploaded file."""
        try:
            image = Image.open(uploaded_file)

            processed = self.preprocess_pil_image(image)

            text = pytesseract.image_to_string(processed)

            return text if text.strip() else "No text found in image"

        except Exception as e:
            st.error(f"OCR Error: {str(e)}")
            return None

    def extract_text_from_pil_image(self, pil_image):
        """Extract text from PIL Image."""
        try:
            processed = self.preprocess_pil_image(pil_image)

            text = pytesseract.image_to_string(processed)

            return text if text.strip() else "No text found in image"

        except Exception as e:
            st.error(f"OCR Error: {str(e)}")
            return None

    def preprocess_pil_image(self, pil_image):
        """Improve image quality for OCR."""
        try:
            img = np.array(pil_image)

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Noise removal
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Thresholding
            _, thresh = cv2.threshold(
                blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )

            return thresh

        except Exception as e:
            st.error(f"Preprocessing Error: {str(e)}")
            return pil_image