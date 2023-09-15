import pytesseract
from PIL import Image

class BuffOCR:
    def read(self, buff):
        # Convert buff to image
        image = Image.fromarray(buff)

        # Read timer
        return int(pytesseract.image_to_string(image))
