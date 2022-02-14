# tassel
Tools to draw images and text with any font on oled-displays in MicroPython

![Photo with test should be here](/docs/demo.jpg "How it looks like in real life.")


## Quick start

### Zero step

Take ESP (I tested only on ESP8266) and install MicroPython

### Images

1.  Convert image with tools/create-image.py

        cd ./tools/
        
    Open create-image.py in yours favorite editor. If you want convert one image:
    
        def init():
        	oneImage("../sources/icon.png","../examples/images/icon.img")

    ...or many icons from a single file located on a grid
    
        def init():
        	groupOfImages(
        		"../sources/icons2.png",
        		"../examples/images/icons.img",
        		(44,44),    # one icon size
        		(35,18),    # indent from left top corner
        		(32,28),    # width and height between border of adjacent icons
        		14,         # number of columns
        		23          #        ...rows
        	)
        
    Then execute
        
        python create-image.py
        
    

2. Upload files to your device from examples folder (examples/images)

        cd ./examples/images/
        ampy --port /dev/ttyUSB0 put boot.py 
        ampy --port /dev/ttyUSB0 put ../../src tassel
        ampy --port /dev/ttyUSB0 put icons.img 
        ampy --port /dev/ttyUSB0 put icon.img
        
        
### Fonts