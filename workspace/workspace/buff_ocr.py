import pytesseract
from PIL import Image
import logging
import os

class BuffOCR:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'buff_ocr.log'))
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def read(self, buff):
        # Extract image data from tuple
        _, image_data = buff

        # Convert image data to image
        image = Image.fromarray(image_data)

        # Save the image for debugging
        image.save(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'buff_image.png'))

        # Read timer
        try:
            timer = int(pytesseract.image_to_string(image))
            self.logger.info(f"OCR result for {buff[0]}: {timer}")
            return timer
        except Exception as e:
            self.logger.error(f"Error reading timer for {buff[0]}: {e}")
            return 0
