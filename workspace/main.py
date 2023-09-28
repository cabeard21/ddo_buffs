import json
import os
import sys
from pathlib import Path

from buff_bar import BuffBar
from buff_detector import BuffDetector
from buff_ocr import BuffOCR
from buff_sorter import BuffSorter
from buff_timer import BuffTimer
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMenu, QSystemTrayIcon, QVBoxLayout,
                             QWidget)

if getattr(sys, 'frozen', False):
    # The application is running as a bundled executable
    DATA_DIR = os.path.join(os.path.expanduser("~"), "DDO Buffs")
else:
    # The application is running as a standard Python script
    DATA_DIR = Path(__file__).resolve().parent

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', str(DATA_DIR))
    return os.path.join(base_path, relative_path)


class MainApp(QWidget):

    def __init__(self):
        super().__init__()
        self.tray_icon = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)  # Adjust this value as needed
        self.setLayout(self.layout)

        # Remove title bar, set background transparent,
        # and make window always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool
                            | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.show()

        self.init_tray_icon()

    def init_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path('icon.ico')))

        tray_menu = QMenu()

        close_action = tray_menu.addAction("Close")
        close_action.triggered.connect(self.close_app)

        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.show()

    def close_app(self):
        self.tray_icon.hide()
        self.close()
        QApplication.quit()

    def update_bars(self):
        # Detect buffs
        buffs = self.buff_detector.detect()

        # Update timers and bars
        for buff, image_data in buffs:
            # Read timer
            time = self.buff_ocr.read(buff, image_data)

            # Update timer
            self.buff_timer.update(buff, time)

            # Update bar
            self.buff_bar.update(buff, self.buff_timer.get_remaining(buff))

        # Sort bars
        sorted_bars = self.buff_sorter.sort(self.buff_bar.bars)

        # Update bars with sorted order
        self.buff_bar.bars = dict(sorted_bars)

        # Reorder the bars in the GUI
        self.buff_bar.reorder_bars(sorted_bars)

        # Display bars
        self.buff_bar.display()

    def main(self):
        # Load config
        with open(DATA_DIR / 'config.json', 'r') as f:
            config = json.load(f)

        # Initialize classes
        buff_dir = resource_path('buffs')
        template_dir = resource_path('templates')
        self.buff_detector = BuffDetector(config['buff_coordinates'], buff_dir,
                                          0.7)
        self.buff_timer = BuffTimer()
        self.buff_ocr = BuffOCR(template_dir)

        # Initialize BuffBar with tkinter root
        stack_buffs = {
            item['name']: item['buffs']
            for item in config['buff_config']['stack_buffs']
        }
        cooldowns = config['buff_config'].get('cooldowns', {})
        self.buff_bar = BuffBar(stack_buffs, cooldowns, str(DATA_DIR))

        # Initialize BuffSorter with buff_order
        buff_order = config['buff_config']['buff_order']
        self.buff_sorter = BuffSorter(buff_order, stack_buffs, str(DATA_DIR))

        # QTimer to update the bars
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_bars)
        self.timer.start(1000)  # Update every second


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.main()
    sys.exit(app.exec_())
