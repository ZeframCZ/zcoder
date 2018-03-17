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

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
TRIG = 17
ECHO = 27
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)



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
font = ImageFont.truetype("/usr/share/fonts/truetype/lato/Lato-Medium.ttf", 25, encoding="unic")
font_mid = ImageFont.truetype("/usr/share/fonts/truetype/lato/Lato-Medium.ttf", 20, encoding="unic")
font_small = ImageFont.truetype("/usr/share/fonts/truetype/lato/Lato-Medium.ttf", 17, encoding="unic")
#font_large = ImageFont.truetype(12)ImageFont.truetype("arial.ttf", fontsize)
#--------------------SET UP PLACEHOLDERS--------------------
update = True
timer = 10
text_rotation = 180
screen_width = 230
dist_sens = False#switch between screens
date = datetime.now()
pulse_end = 0
pulse_start = 0

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
    disp.clear((0, 0, 0))
    # --------------------SWITCH BETWEEN SCREENS--------------------
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    input_state = GPIO.input(16)
    if input_state == False:
        dist_sens = False
        time.sleep(0.2)
    else:
        dist_sens = True
    #--------------------DISTANCE SENSOR DATA SCREEN--------------------
    if (dist_sens == False):
        sens_accX, sens_accY, sens_accZ = motion.accelerometer()

        draw.rectangle((217, 310, 23, 260), outline=(255, 255, 255), fill=(0, 120, 255))

        draw.rectangle((217, 250, 23, 190), outline=(255, 255, 255), fill=(0, 120, 255))
        i = sens_accY * 57.295779513
        w1, h1 = draw.textsize(str(i))
        draw_rotated_text(disp.buffer, str(round(i)), (120 - w1, 220), text_rotation, font,fill=(255, 255, 255))

        GPIO.output(TRIG, False)
        time.sleep(0.1)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
        pulse_duration = (pulse_end - pulse_start)
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        if distance > 2 and distance < 400:  # Check whether the distance is within range
            w1, h1 = draw.textsize(str(distance)+"cm")
            draw_rotated_text(disp.buffer,str(distance - 0.5) + "cm", (120-w1, 280), text_rotation, font, fill=(255, 255, 255))
        else:
            w1, h1 = draw.textsize("Out of range")
            draw_rotated_text(disp.buffer, "Out of range", (120 - w1, 280), text_rotation, font,fill=(255, 0, 0))


    #--------------------MAIN SENSOR DATA--------------------
    if (dist_sens == True):
        #--------------------GET STUFF FROM SENSORS--------------------
        sens_temperature = weather.temperature()
        sens_pressure = weather.pressure()
        sens_light = light.light()
        sens_accX, sens_accY, sens_accZ = motion.accelerometer()
        sens_heading = motion.heading()
        Pz = 1013.25
        P = (sens_pressure/100)
        T = (sens_temperature)
        sens_height = ((((Pz*1/P*1)**(1/5.257*1))-1)*(T+273.15))/0.0065
        sens_distance = 0.0

        #--------------------DRAW STUFF FROM SENSORS--------------------240x320
        #Left up temperature
        w, h = draw.textsize(str(int(sens_temperature)) + " C")
        draw.rectangle((217, 310, 132, 225), outline=(255, 255, 255), fill=(0, 120, 255))
        draw_rotated_text(disp.buffer,str(int(sens_temperature))+" C", (174-w,256-h),text_rotation, font, fill=(255, 255, 255))
        #right up pressure
        w, h = draw.textsize(str(int(sens_pressure/100))+"hPa")
        draw.rectangle((108, 310,23, 225), outline=(255, 255, 255), fill=(0, 120, 255))
        draw_rotated_text(disp.buffer, str(int(sens_pressure/100))+"hPa", (63-w, 256-h), text_rotation, font_mid,fill=(255, 255, 255))#271

        #Left mid light
        w, h = draw.textsize(str(int(sens_light))+"lx")
        draw.rectangle((217, 215,  132, 130), outline=(255, 255, 255), fill=(light.rgb()))
        draw_rotated_text(disp.buffer, str(int(sens_light))+"lx", (174-w, 150-h), text_rotation, font,fill=(255, 255, 255))#171
        #right mid height
        w, h = draw.textsize(str(int(sens_height))+"m")
        draw.rectangle((108, 215, 23, 130), outline=(255, 255, 255), fill=(0, 120, 255))
        draw_rotated_text(disp.buffer, (str(int(sens_height)))+"m", (63-w, 150-h), text_rotation, font_mid,fill=(255, 255, 255))

        # Left down acc
        x1 = 174
        y1 = 35
        x2 = 174
        y2 = 120

        xx1 = 132
        yy1 = 77
        xx2 = 217
        yy2 = 77

        A = y1
        B = y2
        C = sens_accY
        D = ((C * A) + ((1 - C) * B))+(y1-y2)/2
        draw.ellipse((x1 - 10, D - 10, x1 + 10, D + 10), outline=(255, 255, 255), fill=(0, 0, 0))
        A = xx1
        B = xx2
        C = sens_accX
        D = ((C * A) + ((1 - C) * B))+(xx1-xx2)/2
        draw.ellipse((D - 10, yy1 - 10, D + 10, yy2 + 10), outline=(255, 255, 255), fill=(0, 0, 0))

        draw.line((x1, y1, x2, y2), fill=(255, 255, 255), width=(1))  # Y
        draw.line((xx1, yy1, xx2, yy2), fill=(255, 255, 255), width=(1))  # X

        #draw.ellipse((x1 - 10, D - 10, x1 + 10, D + 10), outline=(255, 255, 255), fill=(0, 0, 0))

        #draw_rotated_text(disp.buffer, str(sens_accX)+"/"+str(sens_accY)+"/"+str(sens_accZ), (0,50), text_rotation, font_small, fill=(255, 255, 255))
        # right down compass
        draw.ellipse((23, 35, 108, 120), outline=(255, 255, 255), fill=(0, 120, 255))
        xx = (math.cos(-sens_heading * math.pi / 180) * 40) + 67
        yy = (math.sin(-sens_heading * math.pi / 180) * 40) + 79
        draw.line((67, 79, xx, yy), fill=(0, 255, 0), width = (3))
        xx = (math.cos((-sens_heading+180) * math.pi / 180) * 40) + 67
        yy = (math.sin((-sens_heading+180) * math.pi / 180) * 40) + 79
        draw.line((67, 79, xx, yy), fill=(255, 0, 0), width = (3))



    if (update):
        update = False
    if (timer > 1):
        timer -= 1
    if (timer < 2):
        #disp.clear((0, 0, 0))
        update = True
        timer = 5  # delay time
        date = datetime.now()

    #draw line,date and time
    draw.line((0, 25, 240, 25), fill=(255,255,255))
    w1, h1 = draw.textsize(str(date.day)+"."+str(date.month)+"."+str(date.year)+"  "+str(date.hour)+":"+str(date.minute))
    draw_rotated_text(disp.buffer, str(date.day)+"."+str(date.month)+"."+str(date.year)+"  "+str(date.hour)+":"+str(date.minute)+":"+str(date.min), (120 - w1, 8), text_rotation, font_small, fill=(255, 255, 255))

    disp.display()