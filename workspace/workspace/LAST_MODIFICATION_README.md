The issue seems to be with the OCR reading the time from the buff icon. The OCR might be having trouble reading the time due to the preprocessing steps applied to the image. The current preprocessing steps include converting the image to grayscale, applying adaptive thresholding, dilating, eroding, and resizing the image. These steps might be causing the time text to be lost or distorted, resulting in the OCR not being able to read it.

To fix this issue, we can modify the preprocessing steps in the `BuffOCR` class in the `buff_ocr.py` file. We can try removing the dilation and erosion steps, as these might be causing the text to be lost. We can also try different configurations for the adaptive thresholding and resizing steps.

Here is the modified `buff_ocr.py` file:

buff_ocr.py
