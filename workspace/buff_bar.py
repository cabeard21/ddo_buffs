import json
import logging
import os
from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QProgressBar, QVBoxLayout,
                             QWidget)

BASE = Path(__file__).resolve().parent


class BuffBar(QWidget):

    def __init__(self, stack_buffs=None):
        super().__init__()
        self.mpos = None
        self.bars = {}
        self.logger = self._setup_logger()
        self.stack_buffs = stack_buffs
        self.initUI()
        self.load_position()

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
        self.save_position()

    def save_position(self):
        position = self.pos()
        with open(BASE / 'position.json', 'w') as f:
            json.dump({'x': position.x(), 'y': position.y()}, f)

    def load_position(self):
        try:
            with open(BASE / 'position.json', 'r') as f:
                position = json.load(f)
                self.move(position['x'], position['y'])
        except FileNotFoundError:
            pass

    def update(self, buff, remaining):
        # Check if the buff is part of a stack
        stack_name = next(
            (name
             for name, buffs in self.stack_buffs.items() if buff in buffs),
            None)
        if stack_name:
            # If another buff from the same stack is active, remove it
            for other_buff in self.stack_buffs[stack_name]:
                if other_buff != buff and other_buff in self.bars:
                    self.removeBuffBar(other_buff)
            # Use the stack name for the GUI
            self._update_or_create_buff(buff, remaining)
        else:
            self._update_or_create_buff(buff, remaining)

    def _update_or_create_buff(self, buff, remaining):
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
            # Determine the icon path
            if buff in self.stack_buffs:
                # Use the first buff in the stack as the default icon
                icon_path = str(BASE / f'buffs/{self.stack_buffs[buff][0]}')
            else:
                icon_path = None  # TimerWidget will use the default path
            buffBar = TimerWidget(buff, remaining, self.logger, icon_path)
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

    def reorder_bars(self, sorted_order):
        """
        Reorder the bars based on the sorted order
        """
        for buff, _ in sorted_order:
            if buff in self.bars:
                # Move the widget to the end, effectively reordering it
                self.layout.removeWidget(self.bars[buff])
                self.layout.addWidget(self.bars[buff])
                self.logger.debug(f'Moved {buff} to the end of the layout')

    def display(self):
        self.show()


class TimerWidget(QWidget):
    buffExpired = pyqtSignal(str)

    def __init__(self, buff, remaining, logger, icon_path=None):
        super().__init__()
        self.logger = logger
        self.remaining = remaining
        self.buff = buff
        self.icon_path = icon_path or str(BASE / f'buffs/{self.buff}')
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
