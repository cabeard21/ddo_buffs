import os
import sys

if getattr(sys, 'frozen', False):
    # The application is running as a bundled executable
    SAVE_DIR = os.path.join(os.path.expanduser("~"), ".your_app_name")
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
else:
    # The application is running as a standard Python script
    SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

position_path = os.path.join(SAVE_DIR, 'position.json')
