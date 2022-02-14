# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import uos, machine

import gc, time, ssd1306

gc.collect()

from tassel import *

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=1000000)
ssd = ssd1306.SSD1306_I2C(64, 48, i2c)

font10=TasselFont("font-10.fnt",ssd)
font10.setHeight(10)
font10.letterSpace=0

font14=TasselFont("font-14.fnt",ssd)
font14.setHeight(12)
font14.letterSpace=0

font24=TasselFont("font-24.fnt",ssd)
font24.letterSpace=0


ts = Tassel(ssd)

while(1):
	ssd.fill(0)
	ts.textRect("Проверка длинного текста",(0,0,64,48),font10,1,TESSEL_CENTER | TESSEL_VCENTER | TESSEL_WRAP)
	ssd.show()
	time.sleep(2)
	
	
	ssd.fill(0)
	ts.textRect("Шрифт побольше",(0,0,64,24),font14,1,TESSEL_LEFT | TESSEL_TOP | TESSEL_WRAP)
	ts.textRect("Шрифт поменьше",(0,24,64,24),font10,1,TESSEL_RIGHT | TESSEL_BOTTOM | TESSEL_WRAP)
	ssd.show()
	time.sleep(2)
	
	
	ssd.fill(1)
	ts.textRect("ABC",(0,0,64,48),font24,0,TESSEL_CENTER | TESSEL_VCENTER | TESSEL_WRAP)
	ssd.show()
	time.sleep(2)


ssd.fill(0)
ssd.show()

