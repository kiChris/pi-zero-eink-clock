import datetime
import math
import sys
import time

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("pil(low) not found")

def analogue(time, size):
    """Create an image of an analogue clock.

    Featuring a long thin minute line and a short thick hour line."""

    # create empty image
    img = Image.new('1', size, 255)
    draw = ImageDraw.Draw(img)
    w, h = size
    center = (w / 2, h / 2)

    # convert time values to radian equivalents
    angle_min = -(( time.minute     / 60) * 2 * math.pi) + math.pi / 2
    angle_h   = -(((time.hour % 12) / 12) * 2 * math.pi) + math.pi / 2

    margin = 1
    line_len_h = w / 2 - margin - w/6
    line_len_min = w / 2 - margin
    # draw minute line
    draw.line([center, (line_len_min * math.cos(angle_min) + w/2, line_len_min * (-math.sin(angle_min)) + h/2)], fill=0, width=1)
    # draw hours line
    draw.line([center, (line_len_h   * math.cos(angle_h)   + w/2, line_len_h   * (-math.sin(angle_h))   + h/2)], fill=0, width=2)

    return img

def digital(time, size):
    """Create an image of a digital clock."""

    # create empty image
    img = Image.new('1', size, 255)
    draw = ImageDraw.Draw(img)

    # print the time
    time_text = time.strftime("%H:%M:%S")
    draw.text((0, 0), time_text, fill=0, font=None)

    return img
