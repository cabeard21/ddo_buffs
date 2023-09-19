import logging
import os
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QProgressBar, QVBoxLayout,
                             QWidget)

BASE = Path(__file__).resolve().parent


class BuffBar(QWidget):

    def __init__(self):
        super().__init__()
        self.mpos = None
        self.bars = {}
        self.logger = self._setup_logger()
        self.initUI()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'application.log'))
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(self.layout)
        self._set_window_properties()

    def _set_window_properties(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool
                            | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        self.mpos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mpos:
            diff = event.pos() - self.mpos
            new_pos = self.pos() + diff
            self.move(new_pos)
            self.mpos = event.pos()

    def mouseReleaseEvent(self, event):
        self.mpos = None

    def update(self, buff, remaining):
        if buff in self.bars:
            self._update_existing_buff(buff, remaining)
        else:
            self._create_new_buff(buff, remaining)

    def _update_existing_buff(self, buff, remaining):
        if self.bars[buff].expired:
            self.bars[buff].reset(remaining)
            self.logger.debug(
                f'BuffBar reset buff bar for {buff} with remaining '
                f'time {remaining}')
        else:
            self.bars[buff].progressBar.setValue(int(remaining))
            self.bars[buff].progressBar.setFormat(f'{round(remaining)} s')

    def _create_new_buff(self, buff, remaining):
        if remaining > 0:
            buffBar = TimerWidget(buff, remaining, self.logger)
            self.bars[buff] = buffBar
            self.layout.addWidget(buffBar)
            self.logger.debug(
                f'Created new buff bar for {buff} with remaining '
                f'time {remaining}')

    def removeBuffBar(self, buff):
        if buff in self.bars:
            self.layout.removeWidget(self.bars[buff])
            self.bars[buff].deleteLater()
            del self.bars[buff]
            self.logger.debug(f'Removed buff bar for {buff}')

    def display(self):
        self.show()


class TimerWidget(QWidget):
    buffExpired = pyqtSignal(str)

    def __init__(self, buff, remaining, logger):
        super().__init__()
        self.logger = logger
        self.remaining = remaining
        self.buff = buff
        self.expired = False
        self.initUI()

    def initUI(self):
        self._setup_layout()
        self._add_icon_label()
        self._add_progress_bar()
        self._start_timer()

    def _setup_layout(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(self.layout)

    def _add_icon_label(self):
        self.iconLabel = QLabel(self)
        icon_path = str(BASE / f'buffs/{self.buff}')
        if os.path.exists(icon_path):
            self.iconLabel.setPixmap(QIcon(icon_path).pixmap(22, 22))
        else:
            self.logger.error(f'Icon not found: {icon_path}')
        self.layout.addWidget(self.iconLabel)

    def _add_progress_bar(self):
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(int(self.remaining))
        self.progressBar.setValue(int(self.remaining))
        self.progressBar.setFormat(f'{round(self.remaining)} s')
        self.progressBar.setTextVisible(True)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: #00FF00; }")
        self.layout.addWidget(self.progressBar)

    def _start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(1000)

    def updateProgressBar(self):
        currentValue = self.progressBar.value()
        if currentValue > 0:
            self.progressBar.setValue(currentValue - 1)
            self.progressBar.setFormat(f'{round(currentValue - 1)} s')
        else:
            self._handle_buff_expiry()

    def _handle_buff_expiry(self):
        self.progressBar.setValue(self.progressBar.maximum())
        self.progressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: red }")
        self.progressBar.setFormat('')
        self.logger.debug(f'Buff {self.buff} has expired')
        self.timer.stop()
        self.expired = True
        self.buffExpired.emit(self.buff)

    def reset(self, remaining):
        self.expired = False
        self.remaining = remaining
        self.progressBar.setValue(int(self.remaining))
        self.progressBar.setFormat(f'{round(self.remaining)} s')
        self.progressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: #00FF00; }")
        if not self.timer.isActive():
            self.timer.start(1000)
        self.logger.debug(
            f'TimerWidget reset buff bar for {self.buff} with remaining '
            f'time {remaining}')
