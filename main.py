
import epd2in13
import time
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import clocks

#screen_size = (epd2in13.EPD_WIDTH, epd2in13.EPD_HEIGHT)
screen_size = (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH)
screen_width, screen_height = screen_size

def translate(x, y, w, h):
    return (y, epd2in13.EPD_HEIGHT - x - w)

class Program:
    def __init__(self):
        self.epd = epd2in13.EPD()
        self.reset_to_partial()

    def clear(self):
        screen = Image.new('1', (epd2in13.EPD_WIDTH, epd2in13.EPD_HEIGHT), 255)
        screen_draw = ImageDraw.Draw(screen)
        screen_draw.rectangle((0, 0, epd2in13.EPD_WIDTH, epd2in13.EPD_HEIGHT), fill=255)
        self.epd.clear_frame_memory(0xFF)
        self.epd.set_frame_memory(screen, 0, 0)
        self.epd.display_frame()
        self.epd.clear_frame_memory(0xFF)
        self.epd.set_frame_memory(screen, 0, 0)
        self.epd.display_frame()

    def reset_to_partial(self):
        self.epd.init(self.epd.lut_partial_update)
        self.clear()

    def reset_to_full(self):
        self.epd.init(self.epd.lut_full_update)
        self.clear()

    def run(self):
        print("display image")
        # For simplicity, the arguments are explicit numerical coordinates
        image = Image.open('monocolor.bmp')
        ##
         # there are 2 memory areas embedded in the e-paper display
         # and once the display is refreshed, the memory area will be auto-toggled,
         # i.e. the next action of SetFrameMemory will set the other memory area
         # therefore you have to set the frame memory twice.
        ##
        self.epd.set_frame_memory(image.rotate(180), 0, 0)
        self.epd.display_frame()
        self.epd.set_frame_memory(image.rotate(180), 0, 0)
        self.epd.display_frame()

        print("start displaying clock")
        # start printing stuff
        screen = Image.new('1', (150, 32), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(screen)
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 32)
        last_minute = -1
        second_screen_fix = False
        while (True):
            # time
            draw.rectangle((0, 0, screen_width, screen_height), fill = 255)
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

            digital = clocks.digital(now, (96, 16))
            self.epd.set_frame_memory(digital.rotate(90, expand=1), *translate(64, 0, 96, 16))

           	# display
            self.epd.display_frame()

if __name__ == '__main__':
    program = Program()
    program.run()
