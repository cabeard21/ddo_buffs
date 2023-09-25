import os
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QWidget

BASE = Path(__file__).resolve().parent


class TimerWidget(QWidget):
    buffExpired = pyqtSignal(str)
    cooldownStarted = pyqtSignal(str)

    def __init__(self, buff, remaining, logger, icon_path=None):
        super().__init__()
        self.logger = logger
        self.remaining = remaining
        self.buff = buff
        self.icon_path = icon_path or str(BASE / f'buffs/{self.buff}')
        self.expired = False
        self.in_cooldown = False
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
        self.icon_label = QLabel(self)
        if os.path.exists(self.icon_path):
            self.icon_label.setPixmap(QIcon(self.icon_path).pixmap(22, 22))
        else:
            self.logger.error(f'Icon not found: {self.icon_path}')
        self.layout.addWidget(self.icon_label)

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
            if self.in_cooldown:
                self._end_cooldown()
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
        self.cooldownStarted.emit(self.buff)

    def start_cooldown(self, duration):
        self.in_cooldown = True
        self.progressBar.setMaximum(int(duration))
        self.progressBar.setValue(int(duration))
        self.progressBar.setFormat(f'{round(duration)} s')
        self.progressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: blue }")
        if not self.timer.isActive():
            self.timer.start(1000)
        self.logger.debug(
            f'Started cooldown for {self.buff} with duration {duration} '
            f'seconds')

    def _end_cooldown(self):
        self.in_cooldown = False
        self.progressBar.setValue(self.progressBar.maximum())
        self.progressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: red }")
        self.progressBar.setFormat('')
        self.logger.debug(f'Cooldown for {self.buff} has ended')
        self.timer.stop()

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
