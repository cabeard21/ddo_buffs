import cv2
import numpy as np
import os
import pyautogui

class BuffDetector:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.templates = self.load_templates()

    def load_templates(self):
        templates = {}
        for filename in os.listdir('buffs'):
            if filename.endswith('.png'):
                templates[filename] = cv2.imread('buffs/' + filename, 0)
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

        return buffs

    def capture_screen(self):
        # Capture the screen using pyautogui
        screenshot = pyautogui.screenshot()
        screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return screen
