import cv2
import numpy as np
import os
import pyautogui
import logging

class BuffDetector:
    def __init__(self, coordinates, buff_dir):
        self.coordinates = coordinates
        self.buff_dir = buff_dir
        self.templates = self.load_templates()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('buff_detector.log')
        handler.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def load_templates(self):
        templates = {}
        for filename in os.listdir(self.buff_dir):
            if filename.endswith('.png'):
                templates[filename] = cv2.imread(os.path.join(self.buff_dir, filename), 0)
        return templates

    def detect(self):
        # Capture screen
        screen = self.capture_screen()

        # Detect buffs
        buffs = []
        for name, template in self.templates.items():
            # Use the coordinates to search for the template
            result = cv2.matchTemplate(screen[self.coordinates[1]:self.coordinates[3], self.coordinates[0]:self.coordinates[2]], template, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(result)
            buffs.append((name, max_loc))
            self.logger.info(f"Match template result for {name}: {max_loc}")

        return buffs

    def capture_screen(self):
        # Capture the screen using pyautogui
        screenshot = pyautogui.screenshot()
        # Save the screenshot for troubleshooting
        screenshot.save('screenshot.png')
        # Convert the screenshot to grayscale
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        return screen
