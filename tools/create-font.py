from PIL import Image, ImageDraw, ImageFont
from bitarray import bitarray
import string
import math


def getSymbolTable():
	return "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяЁё←↑→↓↔•‣◦"

def init():	
	convertFont(
		"../sources/Leto-Text-Sans-Defect.otf",
		24,	# fontsize
		2,	# symbols padding
		28	# max symbol height, from top of "Ё" to bottom of "g" (optional)
	)

def convertFont(fontpath, fontsize, symbolpadding, symbolheight=0):
	if symbolheight==0:
		symbolheight = fontsize + symbolpadding*2
	
	respath = "../examples/fonts/font-"+str(fontsize)+".fnt"
	
	font = ImageFont.FreeTypeFont(fontpath, fontsize, encoding='cp1251')
	
	im = Image.new('1', ((fontsize+2)*32,(symbolheight)*16), color=('black'))
	draw_text = ImageDraw.Draw(im)
	
	src = getSymbolTable()
	
	mapcount = len(src)
	map = list(src)
	x,y = 0,0
	for c in range(0,mapcount):
		draw_text.text(
			(x,y+symbolpadding),
			src[c],
			font=font,
			fill=('white')
			)
		w=font.getsize(src[c])[0]
		map[c]=symbolEncode(im,x,y,w,symbolheight)
		x += (fontsize+2)
		if x>=(fontsize+2)*16 :
			y += symbolheight
			x = 0
	
	
	saveMap(map,symbolheight,respath)
	
	loadMap(im,(fontsize+2)*16,0,respath,fontsize+2,symbolheight)
	#testMap(map,im,(fontsize+2)*16,0,fontsize,symbolheight)
	
	im.show()


def symbolEncode(im,x0,y0,w,h):
	bits = bitarray()
	for x in range(x0,x0+w):
		for y in range(y0,y0+h):
			bits.append(im.getpixel((x,y))>0)
	return (bits.tobytes(),w)

def saveMap(map,fontsize,file):
	f = open(file,"wb")
	f.write(fontsize.to_bytes(1, byteorder='big'))
	print("Saving map...")
	index = b""
	font = b""
	pos = 0
	for c in map:
		index += c[1].to_bytes(1, byteorder='big')
		index += pos.to_bytes(2, byteorder='big')
		font += c[0]
		#print(c[0])
		pos += len(c[0])
		#print(pos)
	
	#print(len(index)) // 543, 181 symbol
	#print(pos)
	
	f.write(index)
	f.write(font)
	
	f.close()
	print("...Done")

def loadMap(im,x0,y0,file,ws,wh):
	pixels = im.load()
	x,y = 0,0
	f = open(file,"rb")
	fontsize=int.from_bytes(f.read(1),"big")
	l = len(getSymbolTable())
	index = f.read(l*3)
	pos = 0
	for c in range(0,l):
		w = int.from_bytes(index[c*3:c*3+1],"big")
		pos = int.from_bytes(index[c*3+1:c*3+3],"big")
		#print(w)
		#print(pos)
		#f.read(pos0 - pos)
		#print(w)
		bits = bitarray()
		bits.frombytes(f.read(math.ceil(w*fontsize/8)))
		#print(bits)
		i = 0
		for a in range(x,x+w):
			for b in range(y,y+fontsize):
				if len(bits) <= i : break
				pixels[a+x0,b+y0] = bits[i]
				i += 1
		x += ws
		if x>=ws*16 :
			y += wh
			x = 0
		#pos = pos0
	#print(fontsize)
	f.close()


	
def testMap(map,im,x0,y0,fontsize,symbolheight):
	pixels = im.load()
	x,y = 0,0
	for c in map:
		bits = bitarray()
		bits.frombytes(c[0])
		i = 0
		for a in range(x,x+c[1]):
			for b in range(y,y+symbolheight):
				pixels[a+x0,b+y0] = bits[i]
				i += 1
		#print(c[0])
		#pixels[x+x0,y+y0]=1
		#w=font.getsize(chr(c))[0]
		x += (fontsize+2)
		if x>=(fontsize+2)*16 :
			y += symbolheight
			x = 0


	#s=string.printable
	#for c in range(1025,1104):
#		s+=chr(c)
#	for c in [1025,1105]:
#		s+=chr(c)
#	return s

init()
