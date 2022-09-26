import tkinter as tk

from tkinter import *

windowWidth = "1280"
windowHeight = "720"

root = Tk()
root.title('AI Summarizer')
root.geometry(windowWidth+"x"+windowHeight)

button_1 = Button(root, text="Submit", font=("Helvetica", 32))
button_2 = Button(root, text="Clear", font=("Helvetica", 32))

button_1.grid(column=0, row=0)
button_2.grid(column=1, row=0)

T = Text(root)
T.place(relx=0.5, rely=0.5, anchor=CENTER)

def submitText():

    text = T.get()





root.mainloop()


button1 = tk.Button(text='Get the Square Root', command=getSquareRoot)
canvas1.create_window(200, 180, window=button1)

root.mainloop()