# tassel
Tools to draw images and text with any font on oled-displays in MicroPython

![Photo with test should be here](/docs/demo.jpg "How it looks like in real life.")


# Quick start

## Zero step

Take ESP (I tested only on ESP8266) and install MicroPython

## Images

1.  Convert image with tools/create-image.py

    ```
        cd ./tools/
    ```
        
    Open create-image.py in yours favorite editor. If you want convert one image:
    
    ```
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
    ```
        
    Then execute

    ```        
        python create-image.py
    ```
        
    

2. Upload files to your device from examples folder (examples/images)

    ```
        cd ./examples/images/
        ampy --port /dev/ttyUSB0 put boot.py 
        ampy --port /dev/ttyUSB0 put ../../src tassel
        ampy --port /dev/ttyUSB0 put icons.img 
        ampy --port /dev/ttyUSB0 put icon.img
    ``` 
        
## Fonts

1.  Convert font with tools/create-font.py
    ```
        cd ./tools/
    ```

    Change options in create-font.py. Set font file and font size you need
    
    ```
        def init():	
        	convertFont(
        		"../sources/Leto-Text-Sans-Defect.otf",
        		24,   # fontsize
        		2,    # symbols padding
        		28    # max symbol height, from top of "Ё" to bottom of "g" (optional)
        	)
    ```
    Then execute

    ```        
        python create-image.py
    ```

    > You can change symbols list in function ```getSymbolTable```.
    > Don't forget to change ```TasselSymbols``` in ```src/tassel.py```.
    
    > In current version symbols list is the same in all using fonts

    
2. Upload files to your device from examples folder (examples/fonts)

    ```
        cd ./examples/images/
        ampy --port /dev/ttyUSB0 put boot.py 
        ampy --port /dev/ttyUSB0 put ../../src tassel
        ampy --port /dev/ttyUSB0 put font-7.fnt
        ampy --port /dev/ttyUSB0 put font-10.fnt
        ampy --port /dev/ttyUSB0 put font-14.fnt
        ampy --port /dev/ttyUSB0 put font-24.fnt
    ``` 