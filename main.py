
import epd2in13
import time
import datetime
from PIL import Image, ImageDraw, ImageFont

import clocks

screen_size = (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH)
screen_width, screen_height = screen_size

def translate(x, y, w, h):
    """Convert horizontal coordinates to screen coordinates."""
    return (y, epd2in13.EPD_HEIGHT - x - w)

def center(image_height, item_height):
    return image_height // 2 - item_height // 2

class Program:
    def __init__(self):
        self.epd = epd2in13.EPD()

        self.background = Image.open('monocolor.bmp').rotate(180)

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

    def draw_background(self):
        """Redraw the background image."""
        # set both framebuffers to the image as clock background
        self.epd.set_frame_memory(self.background, 0, 0)
        self.epd.display_frame()
        self.epd.set_frame_memory(self.background, 0, 0)
        self.epd.display_frame()

        # let the image show up
        self.epd.delay_ms(500)

    def run(self):
        """Main loop."""
        print("display image")
        self.draw_background()

        print("start displaying clock")
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 32)
        last_minute = -1

        analogue_refresh = False

        while True:
            # time
            now = datetime.datetime.now()

            # fix for second framebuffer
            if analogue_refresh:
                analogue = clocks.analogue(now, (64, 64))
                self.epd.set_frame_memory(analogue.rotate(90, expand=1), *translate(screen_width // 2 - 64, center(screen_height, 64), *analogue.size))
                analogue_refresh = False

            # analogue clock
            # every minute
            if now.minute != last_minute:
                # clear screen every 15 min
                if (now.minute % 15) == 0:
                    self.reset_to_full()
                    self.set_to_partial()
                    self.draw_background()

                last_minute = now.minute

                # refresh analogue clock every min
                analogue = clocks.analogue(now, (64, 64))
                self.epd.set_frame_memory(analogue.rotate(90, expand=1), *translate(screen_width // 2 - 64, center(screen_height, 64), *analogue.size))
                analogue_refresh = True

            # digital clock
            digital = clocks.digital(now, (48, 16))
            self.epd.set_frame_memory(digital.rotate(90, expand=1), *translate(screen_width // 2, center(screen_height, 16), *digital.size))

           	# display
            self.epd.display_frame()

if __name__ == '__main__':
    program = Program()
    program.run()
