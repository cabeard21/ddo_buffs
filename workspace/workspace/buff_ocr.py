import pytesseract
from PIL import Image
import logging
import os
import cv2

class BuffOCR:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'buff_ocr.log'))
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def preprocess_image(self, image):
        # Check if the image is already in grayscale
        if len(image.shape) == 2:
            gray_image = image
        else:
            # Convert the image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding to the grayscale image
        thresholded_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Resize the image
        resized_image = cv2.resize(thresholded_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        return Image.fromarray(resized_image)

    def read(self, buff):
        # Extract image data from tuple
        _, image_data = buff

        # Preprocess the image
        preprocessed_image = self.preprocess_image(image_data)

        # Save the image for debugging
        preprocessed_image.save(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'buff_image.png'))

        # Read timer
        try:
            # Add a whitelist of characters to the OCR configuration
            timer = pytesseract.image_to_string(preprocessed_image, config='--psm 6 -c tessedit_char_whitelist=0123456789:')
            self.logger.info(f"OCR result for {buff[0]}: {timer}")
            return timer
        except Exception as e:
            self.logger.error(f"Error reading timer for {buff[0]}: {e}")
            return 0
