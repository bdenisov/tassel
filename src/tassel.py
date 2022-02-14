import ssd1306
import os
from math import ceil

TasselSymbols = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяЁё←↑→↓↔•‣◦"
TasselSymbolsCount = len(TasselSymbols)

TESSEL_LEFT = const(0b0000001)
TESSEL_RIGHT = const(0b0000010)
TESSEL_TOP = const(0b0000100)
TESSEL_BOTTOM = const(0b0001000)
TESSEL_CENTER = const(0b0010000)
TESSEL_VCENTER = const(0b0100000)
TESSEL_WRAP = const(0b1000000)

TESSEL_HALF = const(0b0001)
TESSEL_INVERT = const(0b0010)
TESSEL_OPACITY0 = const(0b0100)
TESSEL_OPACITY1 = const(0b1000)


class Tassel:
    def __init__(self, ssd):
        self.ssd=ssd
    
    def show(self):
        if self.ssd is not None:
            self.ssd.show()

    def image(self, path, x, y, color=1, index=1, options=0):
        img = TasselImage(path)
        img.draw(x,y,self.ssd,index,options)


    def text(self, text, x, y, font, color=1):
        font.text(text,x,y,color)

    def textRectCenter(self, text, rect, font, color=1):
        self(text,rect,font,color,TESSEL_CENTER | TESSEL_VCENTER | TESSEL_WRAP)

    def textRectWrap(self, text, x, y, font, color=1):
        self(text,rect,font,color,TESSEL_LEFT | TESSEL_TOP | TESSEL_WRAP)
        
    def textRect(self, text, rect, font, color=1, options=0):
        #self.ssd.text(text,x,y,color)
        
        if self.__opt(options,TESSEL_WRAP):
            words=text.split(" ")
            lw=0
            lines=list()
            line=""
            for w in words:
                m = font.mesure(w)
                if lw + m > rect[2] and lw != 0:
                    lines.append((line,lw))
                    line=""
                    lw=0
                if lw > 0:
                    lw += font.spaceWidth
                    line+=" "
                line += w
                lw += m
            lines.append((line,lw))
            
            if self.__opt(options,TESSEL_VCENTER):
                y = (rect[3]-len(lines)*font.height()) // 2
            elif self.__opt(options,TESSEL_BOTTOM):
                y = rect[3]-len(lines)*font.height()
            else:
                y = 0
            x = 0
            y += rect[1]
            for line in lines:
                if self.__opt(options,TESSEL_CENTER):
                    x=(rect[2]-line[1]) // 2
                elif self.__opt(options,TESSEL_RIGHT):
                    x=rect[2]-line[1]
                font.text(line[0], rect[0] + x, y, color, self.ssd)
                y += font.height()
        else:
            x,y = 0,0
            if self.__opt(options,TESSEL_CENTER):
                x=(rect[2]-font.mesure(text)) // 2
            elif self.__opt(options,TESSEL_RIGHT):
                x=rect[2]-font.mesure(text)
                
            if self.__opt(options,TESSEL_VCENTER):
                y=(rect[3]-font.height()) // 2
            elif self.__opt(options,TESSEL_BOTTOM):
                y=rect[3]-font.height()
                
            font.text(text, rect[0]+x, rect[1]+y, color, self.ssd)
        
        #font.lineHeight()

    def __opt(self,options,opt):
        return options & opt > 0


class TasselImage:
    def __init__(self, path, ssd=None):
        self.ssd=ssd
        self.width=0
        self.height=0
        self.type=-1
        self.f=None
        try:
            self.f=open(path,'rb')
        except:
            print("Error opening file :: %s" % (path))
        else:
            self.type=int.from_bytes(self.f.read(1),"big")
            self.width=int.from_bytes(self.f.read(1),"big")
            self.height=int.from_bytes(self.f.read(1),"big")
            if self.type == 1:
                self.count = int.from_bytes(self.f.read(2),"big")

    def getCount(self):
        return self.count

    def getSize(self):
        return (self.width,self.height)
    
    @micropython.native
    def draw(self, x0, y0, ssd=None, index=0, options=0):
        if self.f is None: return
        if ssd is None:
            ssd=self.ssd
        s = self.getSize()
        if self.type == 0:
            self.f.seek(3,0)
        else:
            self.f.seek(5,0)
        
        if self.type == 1:
            if index >= self.count: return 
            self.f.seek(5+index*ceil(s[0]*s[1]/8),0)
        x,y = 0,0
        opts = (options & TESSEL_HALF > 0, options & TESSEL_INVERT > 0, options & TESSEL_OPACITY0 > 0, options & TESSEL_OPACITY1 > 0)
        for n in range(0,ceil(s[0]*s[1]/8),300):
            blist = self.f.read(300)
            for b in blist:
                for i in range(0,8):
                    self.__setpixel(b,i,x0,y0,x,y,opts,ssd)
                    y += 1
                    if y >= s[1]:
                        y = 0
                        x += 1
                        if x >= s[0]:
                            return

    @micropython.native
    def __setpixel(self,b,i,x0,y0,x,y,opts,ssd):
        if opts[0]:
            if ( x % 2 == 0 and y % 2 == 0 ):
                color = (b >> (7-i)) % 2
                x = x // 2
                y = y // 2
            else: return
        else:
            color = (b >> (7-i)) % 2
        if opts[1]: color = not color
        if (opts[2] and color==0) or (opts[3] and color==1):
            return
        ssd.pixel(x0+x,y0+y,color)
    
    
    def show(self):
        if self.ssd is not None:
            self.ssd.show()
    
    def __del__(self):
        self.f.close()
    

class TasselFont:
    def __init__(self, path, ssd=None):
        self.ssd=ssd
        self.f=open(path,'rb')
        self.fontsize=int.from_bytes(self.f.read(1),"big")
        self.__lineheight=self.fontsize
        self.spaceWidth=2
        self.letterSpace=2
        #print("Font size: "+str(self.fontsize))

    def setHeight(self, lh=0):
        if lh <= 0:
            lh = self.fontsize
        self.__lineheight=lh
        
    def height(self):
        return self.__lineheight

    def text(self, text, x, y, color=1, ssd=None):
        w = 0
        for c in text:
            if c == " " :
                w += self.spaceWidth
                continue
            w += self.symbol(c, x+w, y, color, ssd)+self.letterSpace
    
    def mesure(self, text):
        w = 0
        for c in text:
            if c == " " :
                w += self.spaceWidth
                continue
            w += self.symbolMesure(c)+self.letterSpace
        return w
    
    def symbol(self, char, x0, y0, color=1, ssd=None):
        if ssd is None:
            ssd=self.ssd
        ind = self.symbolIndex(char)
        self.f.seek(1+TasselSymbolsCount*3+ind[1])
        map=bytearray(self.f.read(ceil(ind[0]*self.fontsize/8)))
        x = 0
        y = 0
        for b in map:
            for i in range(0,8):
                if (b >> (7-i)) % 2:
                    ssd.pixel(x0+x,y0+y,color)
                y += 1
                if y >= self.fontsize:
                    y = 0
                    x += 1
                    if x >= ind[0]:
                        break
        return ind[0]

    def symbolMesure(self, char):
        ind = self.symbolIndex(char)
        return ind[0]

    def symbolIndex(self, char):
        d=TasselSymbols.find(char)
        if d == -1:
            return self.symbolIndex("?")
        self.f.seek(1+d*3,0)
        return (int.from_bytes(self.f.read(1),"big"),int.from_bytes(self.f.read(2),"big"))
    
    
    def show(self):
        if self.ssd is not None:
            self.ssd.show()

    
    def __del__(self):
        self.f.close()
