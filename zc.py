#--------------------IMPORT STUFF--------------------
import PIL

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from envirophat import weather
from envirophat import light
from envirophat import motion

import math
#import subprocess
import os

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

#import date
from datetime import datetime

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
#font = ImageFont.load_default()
font = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Thin.ttf', 8)
#font_large = ImageFont.truetype(12)ImageFont.truetype("arial.ttf", fontsize)
#--------------------SET UP PLACEHOLDERS--------------------
update = True
timer = 10
text_rotation = 180
screen_width = 230

#--------------------DEFINE DRAW FUNCTION--------------------
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
while(True):#repeat
    if (update):
        #--------------------GET STUFF FROM SENSORS--------------------
        sens_temperature = weather.temperature()
        sens_pressure = weather.pressure()
        sens_light = light.light()
        sens_accX, sens_accY, sens_accZ = motion.accelerometer()
        sens_heading = motion.heading()
        sens_height = 9999;
        sens_distance = 0.0

        date = datetime.now()

        #--------------------DRAW STUFF FROM SENSORS--------------------240x320

        w1, h1 = draw.textsize("ZCoder 2.0")
        w2, h2 = draw.textsize("" + str(math.floor(sens_temperature)))
        w3, h3 = draw.textsize("" + str(math.floor(sens_pressure)))
        w4, h4 = draw.textsize("" + str(sens_light))
        w5, h5 = draw.textsize("")
        w6, h6 = draw.textsize("X: " + str(math.floor(sens_accX)))
        w7, h7 = draw.textsize("Y: " + str(math.floor(sens_accY)))
        w8, h8 = draw.textsize("Z: " + str(math.floor(sens_accZ)))
        w10, h10 = draw.textsize("Kompas: " + str(sens_heading))
        #w11, h11 = draw.textsize("Vzdalenost: " + str(sens_distance))

        #draw_rotated_text(disp.buffer, "ZCoder 2.0", (screen_width - w1, 310), text_rotation, font,fill=(255, 255, 255))

        #Left up temperature
        draw.rectangle((217, 310, 132, 225), outline=(255, 255, 255), fill=(0, 120, 255))
        draw_rotated_text(disp.buffer,str(math.floor(sens_temperature)), (132-10,225-10),text_rotation, font, fill=(255, 255, 255))
        #right up pressure
        draw.rectangle((108, 310,23, 225), outline=(255, 255, 255), fill=(120, 255, 0))
        draw_rotated_text(disp.buffer, str(math.floor(sens_pressure)), (23-10, 225-10), text_rotation, font,fill=(255, 255, 255))

        #Left mid light
        draw.rectangle((217, 215,  132, 130), outline=(255, 255, 255), fill=(0, 120, 255))
        draw_rotated_text(disp.buffer, str(math.floor(sens_light)), (132-10, 130-10), text_rotation, font,fill=(255, 255, 255))
        #right mid height
        draw.rectangle((108, 215, 23, 130), outline=(255, 255, 255), fill=(120, 255, 0))
        draw_rotated_text(disp.buffer, str(math.floor(sens_height)), (23-10, 130-10), text_rotation, font,fill=(255, 255, 255))

        # Left mid light
        draw.rectangle((217, 120,  132, 35), outline=(255, 255, 255), fill=(0, 120, 255))
        draw_rotated_text(disp.buffer, str(math.floor(sens_light)), (132-10, 35-10), text_rotation, font,fill=(255, 255, 255))
        # right mid height
        draw.rectangle((108, 120, 23, 35), outline=(255, 255, 255), fill=(120, 255, 0))
        draw_rotated_text(disp.buffer, str(math.floor(sens_height)), (23-10, 35-10), text_rotation, font,fill=(255, 255, 255))

        #draw line,date and time
        draw.line((0, 10, 240, 10), fill=(255,255,255))
        draw_rotated_text(disp.buffer, str(date), (50, 0), text_rotation, font,fill=(255, 255, 255))




        disp.display()
        update = False
    ##--------------------DELAY SCREEN UPDATE--------------------
    if (timer > 1):
        timer -= 1
    if (timer < 2):
        disp.clear((0, 0, 0))
        update = True
        timer = 20#delay time