# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import uos, machine

import gc, time, ssd1306

gc.collect()

# import tassel lib
from tassel import *

WIDTH = 64
HEIGHT = 48

# connect to display with I2C bus
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=1000000)
ssd = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# clear screen
ssd.fill(0)

# load image controller
# several icons are stored in this file at once
img=TasselImage("icons.img")

# make some effects with options
ssd.fill(0)
for i in range(0,HEIGHT,2):
    ssd.line(0,i,WIDTH,i,1)
    
img.draw(10,2,ssd,133,TESSEL_OPACITY1 | TESSEL_INVERT)

ssd.show();

time.sleep(2)

# draw one icon in full size
for i in range(0,min(50,img.getCount())):
	ssd.fill(0)
	img.draw(10,2,ssd,i,TESSEL_OPACITY0)
	ssd.show()
	#time.sleep(0.5)
    
time.sleep(2)


# draw four icons in half size
for i in range(50,img.getCount(),4):
	ssd.fill(0)

    # args:
    # first two is coordinates
    # then oled object of ssd1306 driver
    # image index
    # options:
    #   TESSEL_HALF - draw icon in half size
    #   TESSEL_INVERT - invert image
    #   TESSEL_OPACITY0 - skip black (0) pixels when drawing
    #   TESSEL_OPACITY1 - skip white (1) pixels when drawing


	img.draw(10,2,ssd,i,TESSEL_HALF | TESSEL_INVERT)
	img.draw(32,2,ssd,i+1,TESSEL_HALF)
	img.draw(10,24,ssd,i+2,TESSEL_HALF)
	img.draw(32,24,ssd,i+3,TESSEL_HALF)
	ssd.show()
	time.sleep(0.5)

time.sleep(2)
ssd.fill(0)
ssd.show()

