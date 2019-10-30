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
with open('books.txt', 'r') as file:   
    lines = file.read().splitlines()
    for n in range(0, len(lines), 5):
        rf = lines[n]
        title = lines[n+1]
        author = lines[n+2]
        description = lines[n+3]
        image_link = lines[n+4]
        books.append(Book(rf, title, author, description, image_link))

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

col = int(1280/2 - 50)

def open_resize(name, w):
        img = Image.open(name)
        if(w):
            ratio = w/img.size[0]
            h = int(img.size[1]*ratio)
            img = img.resize((w, h), Image.ANTIALIAS)
        return img

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.master.bind('<Escape>', self.goodbye)
        self.master.bind('<Button-1>', self.goodbye)

        self.book_title = Label(self.master, text="", font="Helvetica 22", wraplength=col, justify=LEFT)
        self.book_author = Label(self.master, text="", font="Helvetica 18", wraplength=col, justify=LEFT)
        self.book_description = Label(self.master, text="", font="Helvetica 12", wraplength=col, justify=LEFT)
        self.book_image = Label(self.master, text="", font="Helvetica 14", wraplength=col, justify=LEFT)

        # explanation label
        explanation_text_title = "Identificação por radiofrequência"
        explanation_text_top = """
        RFID ("Radio-Frequency IDentification") é um método de identificação automática através de sinais de rádio, recuperando e armazenando dados remotamente através de dispositivos denominados etiquetas RFID.
        """

        explanation_text_bottom = """
        Passe o RFID de um dos livros no leitor.
        """
        
        explanation_title = Label(self.master, text=explanation_text_title, font="Helvetica 30", wraplength=col, justify=LEFT)
        explanation_body = Label(self.master, text=explanation_text_top, font="Helvetica 18", wraplength=col, justify=LEFT)
        explanation_footer = Label(self.master, text=explanation_text_bottom, font="Helvetica 18", wraplength=col, justify=LEFT)
        
        expimg_file = open_resize('RFID-Arduino.png', col)
        expimg = ImageTk.PhotoImage(expimg_file)
        explanation_picture = Label(self.master, text="", font="Helvetica 18", image=expimg, wraplength=col, justify=LEFT)
        explanation_picture.image = expimg

        self.blank_label = Label(height=1).grid(column=0, row=0)
        explanation_title.grid(column=0, row=1)
        explanation_body.grid(column=0, row=2)
        explanation_picture.grid(column=0, row=3)        
        explanation_footer.grid(column=0, row=4)

        self.book_title.grid(column=1, row=1)
        self.book_author.grid(column=1, row=2)
        self.book_image.grid(column=1, row=3)
        self.book_description.grid(column=1, row=4)

        master.grid_columnconfigure(0, weight=1, uniform='group1')
        master.grid_columnconfigure(1, weight=1, uniform='group1')

    def goodbye(self, event = None):
        print('Exit')
        if use_port:
            port.close()
        root.destroy()

    def checkCard(self):
        root.after(50, self.checkCard)
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
            #print("You book is here:")
            #print(book.rfid, book.title, book.author, book.description, sep='\n')
            self.book_title.configure(text=book.title)
            self.book_author.configure(text=book.author)
            self.book_description.configure(text=book.description)
            #print(book.image_file)

            cover_file = open_resize(book.image_file, 120)
            cover = ImageTk.PhotoImage(cover_file)
            self.book_image.configure(image=cover)
            self.book_image.image = cover

root = Tk()
app = Window(root)
root.wm_title("Leitor de RFID")
root.geometry("1280x720")
root.attributes('-fullscreen', True)
root.after(500, app.checkCard)
root.mainloop()
