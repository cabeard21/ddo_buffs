import logging
import os

import cv2
import numpy as np
import pyautogui


class BuffDetector:

    def __init__(self, coordinates, buff_dir, threshold=0.8):
        self.coordinates = coordinates
        self.buff_dir = buff_dir
        self.templates = self.load_templates()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'application.log'))
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.threshold = threshold

    def load_templates(self):
        templates = {}
        for filename in os.listdir(self.buff_dir):
            if filename.endswith('.png'):
                templates[filename] = cv2.imread(
                    os.path.join(self.buff_dir, filename), 0)
        return templates

    def detect(self):
        # Capture screen
        try:
            screen_gray, screen_color = self.capture_screen()
        except OSError as e:
            self.logger.error(f"Failed to capture screen: {e}")
            return []

        # Detect buffs
        buffs = []
        for name, template in self.templates.items():
            # Use the coordinates to search for the template
            result = cv2.matchTemplate(
                screen_gray[self.coordinates[1]:self.coordinates[3],
                            self.coordinates[0]:self.coordinates[2]], template,
                cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val < self.threshold:
                continue

            # Extract image data
            image_data = screen_gray[max_loc[1]:max_loc[1] + template.shape[0],
                                     max_loc[0]:max_loc[0] + template.shape[1]]

            buffs.append((name, image_data))
            self.logger.debug(
                f"Match template result for {name}: {max_loc} with "
                f"value {max_val}")

            # Draw a red box around the area of interest
            cv2.rectangle(screen_color,
                          (self.coordinates[0], self.coordinates[1]),
                          (self.coordinates[2], self.coordinates[3]),
                          (0, 0, 255), 2)

            # Draw a green box around the match
            cv2.rectangle(screen_color, max_loc,
                          (max_loc[0] + template.shape[1],
                           max_loc[1] + template.shape[0]), (0, 255, 0), 2)

        # Save the screenshot with the boxes
        cv2.imwrite(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'screenshot.png'), screen_color)

        return buffs

    def capture_screen(self):
        # Capture the screen using pyautogui
        screenshot = pyautogui.screenshot()
        # Convert the screenshot to grayscale
        screen_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        # Convert the screenshot to color
        screen_color = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return screen_gray, screen_color
