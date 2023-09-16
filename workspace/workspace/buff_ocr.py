import pytesseract
from PIL import Image

class BuffOCR:
    def read(self, buff):
        # Extract image data from tuple
        _, image_data = buff

        # Convert image data to image
        image = Image.fromarray(image_data)

        # Read timer
        return int(pytesseract.image_to_string(image))
