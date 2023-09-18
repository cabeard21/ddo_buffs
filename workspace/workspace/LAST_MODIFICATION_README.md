The error message "TypeError: unhashable type: 'numpy.ndarray'" indicates that a numpy array is being used as a key in a dictionary. In Python, only immutable types can be used as dictionary keys. The numpy array is mutable and hence cannot be used as a key.

Looking at the code, the error is likely occurring in the `buff_timer.update(buff, time)` line in the `main.py` file. Here, `buff` is a tuple containing a string and a numpy array. The numpy array in this tuple is causing the error.

To fix this, we can modify the `buff` to only include the string (buff name) and not the numpy array (image data). This can be done in the `detect` method of the `BuffDetector` class in the `buff_detector.py` file. Instead of returning a tuple of the buff name and image data, we can just return the buff name.

Here are the modified files:

buff_detector.py
