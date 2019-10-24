#!/usr/bin/env python3
import serial
from serial.tools import list_ports
import time
import math
from tkinter import *

# pip install pillow
from PIL import Image
from PIL import ImageTk

bauld = 115200

for port in list_ports.comports():
    print(port)

dev = '/dev/ttyACM0'
print('Conecting in', dev, ' ...')
port = serial.Serial(dev, bauld, timeout=1)
time.sleep(1)
print('done.')

col = 390
sign_w = 220

def open_resize(name, w):
        img = Image.open(name)
        if(w):
            ratio = w/img.size[0]
            h = int(img.size[1]*ratio)
            img = img.resize((w, h), Image.ANTIALIAS)
        return img

dht = {
        'base': open_resize("base.png", 400),
        'short':  open_resize("short.png", sign_w),
        'long':  open_resize("long.png", sign_w),
        }

def tempToAng(c):
    return (-23/12)*c + 205

def humToAng(h):
    return (-272/100)*h + 225

class Indicator():
    def __init__(self, t='h', cx=0, cy=0, r=0, value=0):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.t = t
        self.value = value
        self.ca = 0
        self.cb = 0
        self.updateCoords()

    def changeValue(self, value):
        self.value = value
        return self.updateCoords()

    def updateCoords(self):
        if self.t == 'h':
            theta = humToAng(self.value)
        if self.t == 't':
            theta = tempToAng(self.value)

        self.ca = self.cx + self.r*math.cos(theta*math.pi/180)
        self.cb = self.cy - self.r*math.sin(theta*math.pi/180)
        return self.coords()

    def coords(self):
        return [self.cx, self.cy, self.ca, self.cb]

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.master.bind('<Escape>', self.goodbye)
        self.master.bind('<Button-1>', self.goodbye)

        self.base = ImageTk.PhotoImage(dht['base'])
        self.short_shaft = ImageTk.PhotoImage(dht['short'])
        self.long_shaft = ImageTk.PhotoImage(dht['long'])

        xcenter = int(1184/2)
        sep=30
        dht1x = xcenter - self.base.width() - sep
        dht2x = xcenter + sep
        dht1y = 0
        dht2y = 0

        # Canvas to draw
        self.canvas = Canvas(master, width=1184, height = self.base.height() , bg='black')

        # Left and right displays
        self.canvas.create_image(dht1x, 0, image=self.base, anchor=NW)
        self.canvas.create_image(dht2x, 0, image=self.base, anchor=NW)

        # Indicator's data
        self.left_temp = Indicator('t', dht1x+int(self.base.width()/2)-1, 200-1, 164, 20)
        self.left_hum = Indicator('h', dht1x+int(self.base.width()/2)-2, 313-3, 60, 0)
        self.right_temp = Indicator('t', dht2x+int(self.base.width()/2) -1, 200-1, 164, 20)
        self.right_hum = Indicator('h', dht2x+int(self.base.width()/2)-2, 313-3, 60, 0)

        # Indicator's lines
        self.left_temp_indicator = self.canvas.create_line(self.left_temp.coords(), width=3, fill='red' )
        self.left_hum_indicator = self.canvas.create_line(self.left_hum.coords(), width=3, fill='red' )
        self.right_temp_indicator = self.canvas.create_line(self.right_temp.coords(), width=3, fill='red' )
        self.right_hum_indicator = self.canvas.create_line(self.right_hum.coords(), width=3, fill='red' )

        left_label = """
        Obter informações sobre o clima tem sido cada vez mais importante em nossa sociedade. Os sensores de temperatura e umidade são ótimas ferramentas para este fim.

        Além da possibilidade meteorológica, podemos monitorar ambientes fechados e acionar aquecedores e desumidificadores, estabilizando o clima local.
        """

        # explanation label
        text = Label(self.master, text=left_label, font="Helvetica 18", wraplength=1000, justify=LEFT)

        self.blank_label = Label(height=10).grid(column=0, row=0)

        #text.grid(column=0, row=0)
        #self.img1.grid(column=0, row=0)
        #self.img2.grid(column=1, row=0)
        self.canvas.grid(column=0, row=1)
        text.grid(column=0, row=2)

        #master.grid_columnconfigure(0, weight=1)
        #master.grid_columnconfigure(1, weight=1)

    def goodbye(self, event = None):
        print('Exit')
        port.close()
        root.destroy()

    def light(self, color):
        pass
        #self.img.configure(image=self.colors[color])

    def checkDistance(self):
        root.after(2000, self.checkDistance)
        port.write(b'c')
        time.sleep(1)
        x = port.readline()
        if(len(x)==0):
            return
        try:
            t1, h1, t2, h2 = x.decode('ascii')[:-2].split(' ')
            print(int(t1), 'C,', int(t2), 'C')
            print(int(h1), '%,', int(h2), '%')
        except:
            print('Error! Content:', x)
            return

        # Changing value
        self.left_temp.changeValue(int(t1))
        self.left_hum.changeValue(int(h1))
        self.right_temp.changeValue(int(t2))
        self.right_hum.changeValue(int(h2))

        # updating indicator's coords
        self.canvas.coords(self.left_temp_indicator, self.left_temp.coords())
        self.canvas.coords(self.left_hum_indicator, self.left_hum.coords())
        self.canvas.coords(self.right_temp_indicator, self.right_temp.coords())
        self.canvas.coords(self.right_hum_indicator, self.right_hum.coords())

root = Tk()
app = Window(root)
root.wm_title("Tkinter window")
root.geometry("1184x624")
#root.attributes('-fullscreen', True)
root.after(500, app.checkDistance)
root.mainloop()

