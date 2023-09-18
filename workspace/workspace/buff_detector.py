import cv2
import numpy as np
import os
import pyautogui
import logging

class BuffDetector:
    # ... rest of the code ...

    def detect(self):
        # ... rest of the code ...

        buffs = []
        for name, template in self.templates.items():
            # ... rest of the code ...

            # Only append the buff name, not the image data
            buffs.append(name)
            self.logger.info(f"Match template result for {name}: {max_loc}")

            # ... rest of the code ...

        return buffs

    # ... rest of the code ...
