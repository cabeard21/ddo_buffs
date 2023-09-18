import logging
import os

import cv2
import numpy as np


class BuffOCR:

    def __init__(self, template_dir, threshold=0.8):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'buff_ocr.log'))
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.templates = self.load_templates(template_dir)
        self.threshold = threshold

    def load_templates(self, template_dir):
        templates = {}
        for filename in os.listdir(template_dir):
            if filename.endswith('.png'):
                templates[filename.replace('.png', '')] = cv2.imread(
                    os.path.join(template_dir, filename), cv2.IMREAD_GRAYSCALE)
        return templates

    def read(self, buff, image_data):
        # Save the image for debugging
        cv2.imwrite(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'buff_image.png'), image_data)

        # Detect all matched positions for each template
        all_detected_positions = {}
        for key, template in self.templates.items():
            result = cv2.matchTemplate(image_data, template,
                                       cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= self.threshold)
            all_detected_positions[key] = list(zip(loc[1], loc[0]))

        # Flatten the dictionary and sort all positions based on x-coordinate
        all_positions_list = [
            (key, pos) for key, positions in all_detected_positions.items()
            for pos in positions
        ]
        sorted_all_positions = sorted(all_positions_list,
                                      key=lambda x: x[1][0])

        # Extract detected time
        detected_time = ''.join([item[0] for item in sorted_all_positions])

        # Convert the detected time to seconds
        try:
            minutes, seconds = map(int, detected_time.split('colon'))
            total_seconds = minutes * 60 + seconds
        except ValueError:
            self.logger.error(f'Error converting detected time to seconds '
                              f'for buff {buff}: {detected_time}')
            total_seconds = 0

        self.logger.debug(f'Detected time for buff {buff}: {detected_time} '
                          f'({total_seconds} seconds)')

        return total_seconds
