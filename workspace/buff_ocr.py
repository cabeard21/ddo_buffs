import logging
import os
import re

import cv2
import numpy as np


def non_maximum_suppression(boxes, scores, threshold=0.5):
    if not boxes:
        return []
    boxes = np.array([(x1, y1, x2 - x1, y2 - y1) for (x1, y1, x2, y2) in boxes])
    areas = boxes[:, 2] * boxes[:, 3]
    order = scores.argsort()[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(boxes[i, 0], boxes[order[1:], 0])
        yy1 = np.maximum(boxes[i, 1], boxes[order[1:], 1])
        xx2 = np.minimum(
            boxes[i, 0] + boxes[i, 2], boxes[order[1:], 0] + boxes[order[1:], 2]
        )
        yy2 = np.minimum(
            boxes[i, 1] + boxes[i, 3], boxes[order[1:], 1] + boxes[order[1:], 3]
        )
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        intersection = w * h
        union = areas[i] + areas[order[1:]] - intersection
        iou = intersection / union
        order = order[np.where(iou <= threshold)[0] + 1]
    return keep


class BuffOCR:
    def __init__(self, template_dir, threshold=0.8):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "application.log")
        )
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.templates = self.load_templates(template_dir)
        self.threshold = threshold

    def load_templates(self, template_dir):
        templates = {}
        for filename in os.listdir(template_dir):
            if filename.endswith(".png"):
                templates[filename.replace(".png", "")] = cv2.imread(
                    os.path.join(template_dir, filename), cv2.IMREAD_GRAYSCALE
                )
        return templates

    def read(self, buff, image_data):
        image_data = image_data[18:72, 0:18]
        all_boxes = []
        all_scores = []
        all_labels = []
        for key, template in self.templates.items():
            result = cv2.matchTemplate(image_data, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= self.threshold)
            for x, y in zip(loc[1], loc[0]):
                all_boxes.append((x, y, x + template.shape[1], y + template.shape[0]))
                all_scores.append(result[y, x])
                all_labels.append(key)
        keep_indices = non_maximum_suppression(
            all_boxes, np.array(all_scores), threshold=0.3
        )
        nms_boxes = [all_boxes[i] for i in keep_indices]
        nms_labels = [all_labels[i] for i in keep_indices]
        sorted_indices = sorted(range(len(nms_boxes)), key=lambda k: nms_boxes[k][0])
        sorted_labels = [nms_labels[i] for i in sorted_indices]

        detected_time = "".join(sorted_labels)

        match = re.fullmatch(r"(\d{1,2})([ms])", detected_time)
        if match:
            value = int(match.group(1))
            unit = match.group(2)
            if unit == "m":
                total_seconds = value * 60
            elif unit == "s":
                total_seconds = value
            else:
                total_seconds = 0
        else:
            # Only do this if regex didn't match (old fallback for colon-based timers)
            try:
                minutes, seconds = map(int, detected_time.split("colon"))
                total_seconds = minutes * 60 + seconds
            except ValueError:
                self.logger.error(
                    f"Error converting detected time to seconds for buff {buff}: "
                    f"{detected_time}"
                )
                total_seconds = 0

        self.logger.debug(
            f"Detected time for buff {buff}: {detected_time} "
            f"({total_seconds} seconds)"
        )
        return total_seconds
