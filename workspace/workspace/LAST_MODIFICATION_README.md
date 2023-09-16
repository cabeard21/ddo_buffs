The request is to change the screenshot to be saved in color instead of grayscale. This will make it easier to see the red and green boxes. However, the screenshot that is being searched for the template must remain grayscale. 

The code that needs to be modified is in the `buff_detector.py` file, specifically in the `detect` and `capture_screen` methods. 

In the `capture_screen` method, the screenshot is captured and converted to grayscale. We need to modify this method to return both the grayscale and color versions of the screenshot. 

In the `detect` method, the grayscale screenshot is used for template matching and the color screenshot is used for drawing boxes and saving the screenshot. 

Here is the modified code:

buff_detector.py
