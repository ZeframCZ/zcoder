#--------------------IMPORT STUFF--------------------
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from envirophat import weather
from envirophat import light
from envirophat import motion

import math

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

#-----REFERENCE STUFF-----
#draw.ellipse((10, 10, 110, 80), outline=(0,255,0), fill=(0,0,255))
#draw.rectangle((10, 90, 110, 160), outline=(255,255,0), fill=(255,0,255))
#draw.line((10, 170, 110, 230), fill=(255,255,255))
#draw.polygon([(10, 275), (110, 240), (110, 310)], outline=(0,0,0), fill=(0,255,255))

#--------------------LOAD DISPLAY STUFF--------------------
DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
disp.begin()
disp.clear((0, 0, 0))
draw = disp.draw()
font = ImageFont.load_default()


update = True
timer = 10

#--------------------START DRAWING STUFF--------------------

def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)
while(True):
    if (update):
        draw_rotated_text(disp.buffer, 'Teplota: '+str(weather.temperature()), (10, 10), 90, font, fill=(255,255,255))
        draw_rotated_text(disp.buffer, 'Tlak: '+str(weather.pressure()), (30, 10), 90, font, fill=(255,255,255))
        draw_rotated_text(disp.buffer, 'Svetlo: '+str(light.light()), (50, 10), 90, font, fill=(255,255,255))
        draw_rotated_text(disp.buffer, 'Akcelerace: {0}'.format(str(math.floor(motion.accelerometer()))), (70, 10), 90, font, fill=(255, 255, 255))
        disp.display()
        update = False
    if (timer > 1):
        timer -= 1
    if (timer < 2):
        disp.clear((0, 0, 0))
        update = True
        timer = 20