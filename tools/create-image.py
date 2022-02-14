from PIL import Image, ImageDraw
from bitarray import bitarray
import string
import math

def init():
	imgpath = "../../firmware/images/full.png"
	respath = "../../firmware/images/full.img"
	
	#oneImage("../../firmware/images/full.png","../../firmware/images/full.img")
	groupOfImages(
		"../../firmware/images/icons2.png",
		"../../firmware/images/icons.img",
		(44,44),
		(35,18),
		(32,28),
		14,
		23
	)


def oneImage(imgpath,respath):
	f = open(respath,'wb')
	im = Image.open(imgpath)
	pixels = im.load()
	type = 0
	w, h = im.size
	f.write(type.to_bytes(1,"big"))
	f.write(w.to_bytes(1,"big"))
	f.write(h.to_bytes(1,"big"))
	f.write(encodeImage(pixels,0,0,(w,h)))	
	im.show()
	f.close()

def groupOfImages(imgpath,respath,size,shift,step,rows,cols,zoom=1):
	im = Image.open(imgpath)
	im2 = Image.new('1', (cols*size[0],rows*size[1]), color=('black'))
	pixels2 = im2.load()
	pixels = im.load()

	type = 1
	f = open(respath,'wb')
	f.write(type.to_bytes(1,"big"))
	f.write((size[0]//zoom).to_bytes(1,"big"))
	f.write((size[1]//zoom).to_bytes(1,"big"))
	f.write((cols*rows).to_bytes(2,"big"))
	
	for r in range(0,rows):
		for c in range(0,cols):
			x0=shift[0]+(step[0]+size[0])*c
			y0=shift[1]+(step[1]+size[1])*r
			for x in range(0,size[0]):
				for y in range(0,size[1]):
					pixels2[c*size[0]+x,r*size[1]+y] = encodePixel(pixels[x0+x,y0+y])
				
			#print(encodeImage(pixels,x0,y0,size,zoom))
			f.write(encodeImage(pixels,x0,y0,size))
			
	im2.show()
	f.close()
	

def animateImage(imgpath,respath):
	im = Image.open(imgpath)
	im.show()
	
	
def encodeImage(pixels,x0,y0,size,zoom=1):
	w,h = size
	bits = bitarray()
	for x in range(x0,x0+w,zoom):
		for y in range(y0,y0+h,zoom):
			bits.append(encodePixel(pixels[x,y]))
	return bits.tobytes()

def encodePixel(p):
	line=150
	return p[0]>line or p[1]>line or p[2]>line

init()
