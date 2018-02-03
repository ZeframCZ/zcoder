#--------------------IMPORT STUFF--------------------
import PIL

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from envirophat import weather
from envirophat import light
from envirophat import motion

import math
import subprocess

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
#--------------------SET UP PLACEHOLDERS--------------------
update = True
timer = 10
text_rotation = 180
screen_width = 240

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
        cpu_temp = (subprocess.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"]))
        #--------------------DRAW STUFF FROM SENSORS--------------------240x320
        #get width of texts

        w1,h1 = draw.textsize("ZCoder 2.0")
        w2, h2 = draw.textsize("Teplota: "+str(math.floor(sens_temperature)))
        w3, h3 = draw.textsize("Tlak: "+str(math.floor(sens_pressure)))
        w4, h4 = draw.textsize("Svetlo: "+str(sens_light))
        w5, h5 = draw.textsize("Akcelerace")
        w6, h6 = draw.textsize("X: " + str(math.floor(sens_accX)))
        w7, h7 = draw.textsize("Y: " + str(math.floor(sens_accY)))
        w8, h8 = draw.textsize("Z: " + str(math.floor(sens_accZ)))

        draw_rotated_text(disp.buffer, "ZCoder 2.0", (screen_width-w1,                                    310), text_rotation, font,fill=(255, 255, 255))

        draw_rotated_text(disp.buffer, "Teplota: "+str(math.floor(sens_temperature)), (screen_width-w2,   270), text_rotation, font, fill=(255,255,255))
        draw_rotated_text(disp.buffer, "Teplota CPU: " + str(cpu_temp), (screen_width - w2,               230),text_rotation, font, fill=(255, 255, 255))

        draw_rotated_text(disp.buffer, "Tlak: "+str(math.floor(sens_pressure)), (screen_width-w3,         250), text_rotation, font, fill=(255,255,255))
        draw_rotated_text(disp.buffer, "Svetlo: "+str(sens_light), (screen_width-w4,                      210), text_rotation, font, fill=(255,255,255))

        draw_rotated_text(disp.buffer, "Akcelerace", (screen_width-w5,                                    100), text_rotation, font, fill=(255, 255, 255))
        draw_rotated_text(disp.buffer, "X: " + str(math.floor(sens_accX)), (screen_width-w6,              80), text_rotation, font, fill=(255, 255, 255))
        draw_rotated_text(disp.buffer, "Y: " + str(math.floor(sens_accY)), (screen_width-w7,              60), text_rotation, font, fill=(255, 255, 255))
        draw_rotated_text(disp.buffer, "Z: " + str(math.floor(sens_accZ)), (screen_width-w8,              40), text_rotation, font, fill=(255, 255, 255))
        disp.display()
        update = False
    ##--------------------DELAY SCREEN UPDATE--------------------
    if (timer > 1):
        timer -= 1
    if (timer < 2):
        disp.clear((0, 0, 0))
        update = True
        timer = 20#delay time