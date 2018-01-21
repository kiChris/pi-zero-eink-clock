
import epd2in13
import time
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import clocks

screen_size = (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH)
screen_width, screen_height = screen_size

def translate(x, y, w, h):
    """Convert horizontal coordinates to screen coordinates."""
    return (y, epd2in13.EPD_HEIGHT - x - w)

class Program:
    def __init__(self):
        self.epd = epd2in13.EPD()

        # need full for proper screen refresh
        self.reset_to_full()

        self.set_to_partial()

    def clear(self):
        """Clear the screen."""
        # create empty image
        screen = Image.new('1', (epd2in13.EPD_WIDTH, epd2in13.EPD_HEIGHT), 255)

        # clear both framebuffers
        self.epd.clear_frame_memory(0xFF)
        self.epd.set_frame_memory(screen, 0, 0)
        self.epd.display_frame()
        self.epd.clear_frame_memory(0xFF)
        self.epd.set_frame_memory(screen, 0, 0)
        self.epd.display_frame()

    def set_to_partial(self):
        """Enable partial refresh."""
        self.epd.init(self.epd.lut_partial_update)

    def set_to_full(self):
        """Enable full refresh."""
        self.epd.init(self.epd.lut_full_update)

    def reset_to_partial(self):
        """Enable partial refresh and clear the screen."""
        self.set_to_partial()
        self.clear()

    def reset_to_full(self):
        """Enable full refresh and clear the screen."""
        self.set_to_full()
        self.clear()

    def run(self):
        """Main loop."""
        print("display image")
        image = Image.open('monocolor.bmp')

        # set both framebuffers to the image as clock background
        self.epd.set_frame_memory(image.rotate(180), 0, 0)
        self.epd.display_frame()
        self.epd.set_frame_memory(image.rotate(180), 0, 0)
        self.epd.display_frame()

        # let the image show up
        self.epd.delay_ms(800)

        print("start displaying clock")
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 32)
        last_minute = -1

        # hack to have the analogue clock update on both framebuffers every minute
        second_screen_fix = False

        while True:
            # time
            now = datetime.datetime.now()

            # analogue clock
            if second_screen_fix or last_minute != now.minute:
                last_minute = now.minute
                if not second_screen_fix:
                    second_screen_fix = True
                else:
                    second_screen_fix = False
                analogue = clocks.analogue(now, (64, 64))
                self.epd.set_frame_memory(analogue.rotate(90, expand=1), *translate(0, 0, 64, 64))

            # digital clock
            digital = clocks.digital(now, (96, 16))
            self.epd.set_frame_memory(digital.rotate(90, expand=1), *translate(64, 0, 96, 16))

           	# display
            self.epd.display_frame()

if __name__ == '__main__':
    program = Program()
    program.run()
