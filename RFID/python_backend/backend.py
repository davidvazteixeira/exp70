#!/usr/bin/env python3
import serial
from serial.tools import list_ports
import time
import math
from tkinter import *

# pip install pillow
from PIL import Image
from PIL import ImageTk

from books import Book

books = []
books.append(Book('9B4E2F0B000000000000', 'O Livro Vermelho Misterioso', 'Lucifer', 'Livro proibido sobre os rituais macabros.', 'red.png'))
books.append(Book('A9959656000000000000', 'O Verde das Árvores', 'Madeirinha', 'História infantil pra boi dormir.', 'green.png'))
books.append(Book('09338756000000000000', 'Azul como o Céu', 'Astrogildo', 'Catálogo de anos de observação celeste sem observar nada.', 'blue.png'))
books.append(Book('DB9F960B000000000000', 'Receitas de Alimentos Amarelos', 'Chef Jaune', 'De délicieuses recettes françaises accompagnées de la belle nourriture jaune.', 'yellow.png'))

def search_book(rfid):
    global books
    for book in books:
        if book.rfid == rfid:
            return book
    return None

bauld = 115200

for port in list_ports.comports():
    print(port)

use_port = True

if use_port:
    dev = '/dev/ttyACM0'
    print('Conecting in', dev, ' ...')
    port = serial.Serial(dev, bauld, timeout=1)
    time.sleep(1)
    print('done.')

col = 1184/2 - 10
sign_w = 220

def open_resize(name, w):
        img = Image.open(name)
        if(w):
            ratio = w/img.size[0]
            h = int(img.size[1]*ratio)
            img = img.resize((w, h), Image.ANTIALIAS)
        return img

#dht = {
#        'base': open_resize("base.png", 400),
#        'short':  open_resize("short.png", sign_w),
#        'long':  open_resize("long.png", sign_w),
#        }

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.master.bind('<Escape>', self.goodbye)
        self.master.bind('<Button-1>', self.goodbye)

        #self.short_shaft = ImageTk.PhotoImage(dht['short'])
        #self.long_shaft = ImageTk.PhotoImage(dht['long'])

#        xcenter = int(1184/2)
#        sep=30
#        dht1x = xcenter - self.base.width() - sep
#        dht2x = xcenter + sep
#        dht1y = 0
#        dht2y = 0

        self.book_title = Label(self.master, text="", font="Helvetica 40", wraplength=500, justify=LEFT)
        self.book_author = Label(self.master, text="", font="Helvetica 35", wraplength=500, justify=LEFT)
        self.book_description = Label(self.master, text="", font="Helvetica 25", wraplength=500, justify=LEFT)
        self.book_image = Label(self.master, text="", font="Helvetica 16", wraplength=500, justify=LEFT)

        # explanation label
        explanation_title_text = "Leitores de RFID"
        explanation_text = """
        Aqui tem um texto explicativo muito longo e pouco objetivo que o Nilton não vai gostar.
        """
        explanation_title = Label(self.master, text=explanation_title_text, font="Helvetica 40", wraplength=col, justify=LEFT)
        explanation = Label(self.master, text=explanation_text, font="Helvetica 35", wraplength=col, justify=LEFT)

        self.blank_label = Label(height=1).grid(column=0, row=0)
        explanation_title.grid(column=0, row=1)
        explanation.grid(column=0, row=2)

        self.book_title.grid(column=1, row=1)
        self.book_author.grid(column=1, row=2)
        self.book_image.grid(column=1, row=3)
        self.book_description.grid(column=1, row=4)

        #text.grid(column=0, row=0)
        #self.img1.grid(column=0, row=0)
        #self.img2.grid(column=1, row=0)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

    def goodbye(self, event = None):
        print('Exit')
        if use_port:
            port.close()
        root.destroy()

    def checkCard(self):
        root.after(1000, self.checkCard)
        if not use_port:
            return

        if not port.in_waiting:
            return

        rfid = port.readline()
        try:
            rfid = rfid.decode('ascii')[:-2]
        except:
            print(rfid)
            print('Some error in conversion!')
            return

        if(len(rfid) != 20):
            print(rfid)
            print('Some error in data reception!')
            return

        # Here the card is converted and has 20 chars
        book = search_book(rfid)

        if(book):
            print("You book is here:")
            print(book.rfid, book.title, book.author, book.description, sep='\n')
            self.book_title.configure(text=book.title)
            self.book_author.configure(text=book.author)
            self.book_description.configure(text=book.description)
            print(book.image_file)


            cover_file = open_resize(book.image_file, 200)
            cover = ImageTk.PhotoImage(cover_file)
            self.book_image.configure(image=cover)
            self.book_image.image = cover

root = Tk()
app = Window(root)
root.wm_title("Tkinter window")
root.geometry("1184x624")
#root.attributes('-fullscreen', True)
root.after(500, app.checkCard)
root.mainloop()
