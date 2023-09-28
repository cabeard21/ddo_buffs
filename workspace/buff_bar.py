import json
import logging
import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from timer_widget import TimerWidget


class BuffBar(QWidget):

    def __init__(self, stack_buffs=[], cooldowns={}, data_dir=None):
        super().__init__()
        self.data_dir = data_dir or str(Path(__file__).resolve().parent)

        self.mpos = None
        self.bars = {}
        self.logger = self._setup_logger()
        self.stack_buffs = stack_buffs
        self.cooldowns = cooldowns
        self.initUI()
        self.load_position()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            os.path.join(self.data_dir, 'application.log'))
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
        with open(os.path.join(self.data_dir, 'position.json'), 'w') as f:
            json.dump({'x': position.x(), 'y': position.y()}, f)

    def load_position(self):
        try:
            with open(os.path.join(self.data_dir, 'position.json'), 'r') as f:
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
                icon_path = str(self.data_dir /
                                f'buffs/{self.stack_buffs[buff][0]}')
            else:
                icon_path = None  # TimerWidget will use the default path
            buffBar = TimerWidget(buff, remaining, self.logger, icon_path)
            self.bars[buff] = buffBar
            self.layout.addWidget(buffBar)
            buffBar.cooldownStarted.connect(self.start_buff_cooldown)
            self.logger.debug(
                f'Created new buff bar for {buff} with remaining '
                f'time {remaining}')

    def start_buff_cooldown(self, buff):
        cooldown_duration = self.cooldowns.get(buff, 0)
        if cooldown_duration > 0:
            self.bars[buff].start_cooldown(cooldown_duration)

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

    def display(self):
        self.show()
