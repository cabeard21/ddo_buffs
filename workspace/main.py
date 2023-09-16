import json
from buff_detector import BuffDetector
from buff_timer import BuffTimer
from buff_bar import BuffBar
from buff_sorter import BuffSorter
from buff_ocr import BuffOCR
from pathlib import Path

BASE = Path(__file__).resolve().parent

def main():
    # Load area of interest coordinates
    with open(BASE / 'coordinates.json', 'r') as f:
        coordinates = json.load(f)

    # Initialize classes
    buff_dir = BASE / 'buffs'
    buff_detector = BuffDetector(coordinates, buff_dir)
    buff_timer = BuffTimer()
    buff_bar = BuffBar()
    buff_sorter = BuffSorter()
    buff_ocr = BuffOCR()

    # Main loop
    while True:
        # Detect buffs
        buffs = buff_detector.detect()

        # Update timers and bars
        for buff in buffs:
            # Read timer
            time = buff_ocr.read(buff)

            # Update timer
            buff_timer.update(buff, time)

            # Update bar
            buff_bar.update(buff, buff_timer.get_remaining(buff))

        # Sort bars
        buff_sorter.sort(buff_bar.bars)

        # Display bars
        buff_bar.display()

if __name__ == "__main__":
    main()
