import json
from buff_detector import BuffDetector
from buff_timer import BuffTimer
from buff_bar import BuffBar
from buff_sorter import BuffSorter
from buff_ocr import BuffOCR
from pathlib import Path

BASE = Path(__file__).resolve().parent

def main():
    # ... rest of the code ...

    while True:
        # Detect buffs
        buffs = buff_detector.detect()

        # Update timers and bars
        for buff_name in buffs:
            # Read timer
            time = buff_ocr.read(buff_name)

            # Update timer
            buff_timer.update(buff_name, time)

            # Update bar
            buff_bar.update(buff_name, buff_timer.get_remaining(buff_name))

        # ... rest of the code ...

if __name__ == "__main__":
    main()
