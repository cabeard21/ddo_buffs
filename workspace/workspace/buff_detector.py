import cv2
import numpy as np
import os
import pyautogui
import logging

class BuffDetector:
    # ... existing code ...

    def detect(self):
        # Capture screen
        screen_gray, screen_color = self.capture_screen()

        # Detect buffs
        buffs = []
        for name, template in self.templates.items():
            # Use the coordinates to search for the template
            result = cv2.matchTemplate(screen_gray[self.coordinates[1]:self.coordinates[3], self.coordinates[0]:self.coordinates[2]], template, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(result)
            
            # Extract image data
            image_data = screen_gray[max_loc[1]:max_loc[1] + template.shape[0], max_loc[0]:max_loc[0] + template.shape[1]]

            buffs.append((name, image_data))
            self.logger.info(f"Match template result for {name}: {max_loc}")

            # ... existing code ...

        return buffs
