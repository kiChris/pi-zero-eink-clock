import datetime
import math
import sys
import time

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("pil(low) not found")

# get a font - location depends on OS so try a couple of options
# failing that the default of None will just use a default font
_clock_font = None
try:
    _clock_font = ImageFont.truetype("arial.ttf", 20)
except IOError:
    try:
        _clock_font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 20)
    except IOError:
        pass

def analogue(time, size):
    img = Image.new('1', size, 255)
    draw = ImageDraw.Draw(img)
    w, h = size
    center = (w / 2, h / 2)
    angle_min = -((time.minute/60) * 2 * math.pi) + math.pi / 2
    angle_h = -((time.hour/24) * 2 * math.pi) + math.pi / 2

    margin = 1
    line_len_h = w / 2 - margin - w/6
    line_len_min = w / 2 - margin
    # minutes
    draw.line([center, (line_len_min * math.cos(angle_min) + w/2, line_len_min * (-math.sin(angle_min)) + h/2)], fill=0, width=1)
    # hours
    draw.line([center, (line_len_h   * math.cos(angle_h)   + w/2, line_len_h   * (-math.sin(angle_h))   + h/2)], fill=0, width=2)

    return img

def digital(time, size):
    img = Image.new('1', size, 255)
    draw = ImageDraw.Draw(img)
    time_text = time.strftime("%H:%M:%S")
    draw.text((0, 0), time_text, fill=0, font=None)
    return img
