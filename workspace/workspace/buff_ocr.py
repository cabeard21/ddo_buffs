import pytesseract
from PIL import Image
import logging
import os
import cv2
import numpy as np

class BuffOCR:
    def __init__(self, template_dir):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'buff_ocr.log'))
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)
        self.templates = self.load_templates(template_dir)

    def load_templates(self, template_dir):
        templates = {}
        for filename in os.listdir(template_dir):
            if filename.endswith('.png'):
                templates[filename] = cv2.imread(os.path.join(template_dir, filename), cv2.IMREAD_GRAYSCALE)
        return templates

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

        return resized_image

    def read(self, buff):
        # Extract image data from tuple
        _, image_data = buff

        # Preprocess the image
        preprocessed_image = self.preprocess_image(image_data)

        # Save the image for debugging
        cv2.imwrite(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'buff_image.png'), preprocessed_image)

        # Read timer
        try:
            timer = ""
            for name, template in self.templates.items():
                result = cv2.matchTemplate(preprocessed_image, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                self.logger.debug(f"Template matching value for {name}: {max_val}")
                if max_val > 0.8:  # Lowered the threshold
                    timer += name.replace('.png', '').replace('colon', ':')
            self.logger.info(f"Template matching result for {buff[0]}: {timer}")
            return timer
        except Exception as e:
            self.logger.error(f"Error reading timer for {buff[0]}: {e}")
            return 0
