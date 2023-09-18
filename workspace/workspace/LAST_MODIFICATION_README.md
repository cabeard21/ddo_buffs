The issue seems to be in the `read` function of the `BuffOCR` class in the `buff_ocr.py` file. The function is trying to match the preprocessed buff image with the templates and if the match value is greater than 0.95, it considers it a match. However, the threshold of 0.95 might be too high causing some matches to be missed. 

We can try to lower the threshold to see if it improves the matching. Also, we can add a debug log to print the max_val for each template matching to help us understand the matching values better.

Here is the modified `buff_ocr.py` file:

buff_ocr.py
