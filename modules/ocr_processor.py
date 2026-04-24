import pytesseract
from PIL import Image
import cv2
import numpy as np
from config import STOPWORDS

class OCRProcessor:
    def __init__(self):
        # Make sure Tesseract is installed on system
        pass
    
    def extract_text_from_image(self, image_path):
        """Extract text from image using OCR"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            
            # Get confidence
            data = pytesseract.image_to_data(image)
            
            return text.strip(), True, "OCR completed"
        except Exception as e:
            return "", False, f"OCR Error: {str(e)}"
    
    def extract_text_from_numpy_array(self, image_array):
        """Extract text from numpy array (camera feed)"""
        try:
            text = pytesseract.image_to_string(image_array)
            return text.strip(), True, "OCR completed"
        except Exception as e:
            return "", False, f"OCR Error: {str(e)}"
    
    def preprocess_image(self, image_path):
        """Preprocess image for better OCR accuracy"""
        try:
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Thresholding
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
            
            # Denoising
            denoised = cv2.fastNlMeansDenoising(thresh)
            
            # Dilation
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            dilated = cv2.dilate(denoised, kernel, iterations=1)
            
            return dilated, True, "Preprocessing completed"
        except Exception as e:
            return None, False, f"Error: {str(e)}"
    
    def extract_keywords_from_ocr(self, text, top_n=10):
        """Extract keywords from OCR text"""
        from collections import Counter
        
        words = text.lower().split()
        filtered = [w for w in words if w not in STOPWORDS and len(w) > 3]
        keywords = Counter(filtered).most_common(top_n)
        
        return [w[0] for w in keywords]