from PIL import Image, ImageDraw

class BuffBar:
    def __init__(self):
        self.bars = {}

    def update(self, buff, remaining):
        # Create bar
        bar = Image.new('RGB', (100, 20), color=(0, 255, 0))
        draw = ImageDraw.Draw(bar)

        # Draw remaining time
        draw.rectangle([(0, 0), (remaining, 20)], fill=(255, 0, 0))

        self.bars[buff] = bar

    def display(self):
        for buff, bar in self.bars.items():
            bar.show()
