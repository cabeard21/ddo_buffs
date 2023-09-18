import logging
import os
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QWidget

BASE = Path(__file__).resolve().parent


class BuffBar(QWidget):

    def __init__(self):
        super().__init__()
        self.bars = {}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'buff_bar.log'))
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        # (left, top, right, bottom)
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(self.layout)

        # Set properties for transparency and always-on-top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool
                            | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def update(self, buff, remaining):
        # If the buff bar already exists, update its value
        if buff in self.bars:
            if remaining > 0:
                self.bars[buff].progressBar.setValue(round(remaining))
                self.logger.debug(f'Updated buff bar for {buff} with '
                                  f'remaining time {remaining}')
        else:
            # Create a new buff bar if remaining time is greater than 0
            if remaining > 0:
                buffBar = TimerWidget(buff, self.logger)
                buffBar.progressBar.setValue(round(remaining))
                self.bars[buff] = buffBar
                self.layout.addWidget(buffBar)
                self.logger.debug(f'Created new buff bar for {buff} with '
                                  f'remaining time {remaining}')

    def display(self):
        self.show()


class TimerWidget(QWidget):

    def __init__(self, buff, logger):
        super().__init__()
        self.logger = logger
        self.initUI(buff)

    def initUI(self, buff):
        self.layout = QHBoxLayout()
        # (left, top, right, bottom)
        self.layout.setContentsMargins(10, 0, 10, 0)

        # Icon for the timer
        self.iconLabel = QLabel(self)
        icon_path = str(BASE / f'buffs/{buff}')
        if os.path.exists(icon_path):
            self.iconLabel.setPixmap(QIcon(icon_path).pixmap(22, 22))
        else:
            self.logger.error(f'Icon not found: {icon_path}')
        self.layout.addWidget(self.iconLabel)

        # Progress bar for the timer
        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(100)
        self.progressBar.setTextVisible(False)  # Remove timer text
        self.layout.addWidget(self.progressBar)

        self.setLayout(self.layout)

        # QTimer to update the progress bar
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(1000)  # Update every second

    def updateProgressBar(self):
        currentValue = self.progressBar.value()
        if currentValue > 0:
            self.progressBar.setValue(currentValue - 1)
        else:
            self.timer.stop()
