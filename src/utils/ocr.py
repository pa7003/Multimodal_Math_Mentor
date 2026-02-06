import easyocr
import io
from PIL import Image
import numpy as np

class OCRProcessor:
    def __init__(self, languages=['en']):
        # Initialize EasyOCR reader
        # gpu=False to be safe on all environments, set True if available
        self.reader = easyocr.Reader(languages, gpu=False)

    def process_image(self, image_input):
        """
        Process an image (PIL Image or bytes) and return extracted text.
        """
        try:
            if isinstance(image_input, bytes):
                image = Image.open(io.BytesIO(image_input))
            else:
                image = image_input

            # Convert PIL image to numpy array for EasyOCR
            image_np = np.array(image)
            
            # EasyOCR expects BGR or RGB? It handles standard numpy arrays (RGB usually fine)
            # Run inference
            results = self.reader.readtext(image_np)
            
            # Join results
            extracted_text = " ".join([res[1] for res in results])
            
            # Basic confidence check (average of confidence scores)
            if results:
                avg_confidence = sum([res[2] for res in results]) / len(results)
            else:
                avg_confidence = 0.0
                
            return {
                "text": extracted_text,
                "confidence": avg_confidence,
                "details": results
            }
        except Exception as e:
            return {
                "text": "",
                "confidence": 0.0,
                "error": str(e)
            }
