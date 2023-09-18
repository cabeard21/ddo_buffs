import json
import sys
from pathlib import Path

from buff_bar import BuffBar
from buff_detector import BuffDetector
from buff_ocr import BuffOCR
from buff_sorter import BuffSorter
from buff_timer import BuffTimer
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

BASE = Path(__file__).resolve().parent

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)  # Adjust this value as needed
        self.setLayout(self.layout)

        # Remove title bar, set background transparent, and make window always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.show()

    def update_bars(self):
        # Detect buffs
        buffs = self.buff_detector.detect()

        # Update timers and bars
        for buff, image_data in buffs:
            # Read timer
            time = self.buff_ocr.read(image_data)

            # Update timer
            self.buff_timer.update(buff, time)

            # Update bar
            self.buff_bar.update(buff, self.buff_timer.get_remaining(buff))

        # Sort bars
        sorted_bars = self.buff_sorter.sort(self.buff_bar.bars)

        # Update bars with sorted order
        self.buff_bar.bars = dict(sorted_bars)

        # Display bars
        self.buff_bar.display()

    def main(self):
        # Load area of interest coordinates
        with open(BASE / 'coordinates.json', 'r') as f:
            coordinates = json.load(f)

        # Initialize classes
        buff_dir = BASE / 'buffs'
        template_dir = BASE / 'templates'
        self.buff_detector = BuffDetector(coordinates, buff_dir, 0.5)
        self.buff_timer = BuffTimer()
        self.buff_sorter = BuffSorter()
        self.buff_ocr = BuffOCR(template_dir)

        # Initialize BuffBar with tkinter root
        self.buff_bar = BuffBar()

        # QTimer to update the bars
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_bars)
        self.timer.start(1000)  # Update every second

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.main()
    sys.exit(app.exec_())


