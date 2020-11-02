import Tkinter as tk
from PIL import Image, ImageTk
import PIL.Image
import Settings as s

from Tkinter import *

#
# def change_color():
#     current_color = box.cget("background")
#     next_color = "green" if current_color == "red" else "red"
#     box.config(background=next_color)
#     root.after(1000, change_color)
#
# root = Tk()-
# image = PIL.Image.open('Pictures//background.jpg')
# photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
# background_label =tk.Label(image=photo_image).place(x=0, y=0, relwidth=1, relheight=1)
# box = Text(root, background="green", height=2, width=30)
# box.pack()
# box.insert(tk.END, "Just a text Widget\nin two lines\n")
# box2 = Text(root, background="green")
# box2.pack()
# change_color()
# root.mainloop()

import tkMessageBox
import Tkinter

#
# class FullScreenApp(object):
#     def __init__(self, master, **kwargs):
#         self.master=master
#         pad=3
#         self._geom='200x200+0+0'
#         master.geometry("{0}x{1}+0+0".format(
#             master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
#         master.bind('<Escape>',self.toggle_geom)
#     def toggle_geom(self,event):
#         geom=self.master.winfo_geometry()
#         print(geom,self._geom)
#         self.master.geometry(self._geom)
#         self._geom=geom
#
# if __name__ == "__main__":
#
#     top = Tkinter.Tk()
#     image1 =  PIL.Image.open('Pictures//tryagain.jpg')
#     photo_image1 = ImageTk.PhotoImage(image1)
#     background_label = tk.Label(image=photo_image1).place(relwidth=1, relheight=1)
#
#     image2 = PIL.Image.open('Pictures//tryagainright2.jpg')
#     photo_image2 = ImageTk.PhotoImage(image2)
#     B = tk.Button(background_label, image=photo_image2).pack()
#     # B = Tkinter.Button(top, text ="Hello", command = helloCallBack)
#     #
#     # B.pack()
#     # B.place(height=350, width=350, x=790, y=285)
#
#     app = FullScreenApp(top)
#     top.mainloop()

from Tkinter import *

root = Tk()
root.title('Simple Calculator')
#root.geometry("400x400")



e = Entry(root, width=35, borderwidth=5)
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
# e.insert(0, "Enter Your Name: ")

button_1 = Button(root, text="1", padx=40, pady=20)
button_2 = Button(root, text="2", padx=40, pady=20)
button_3 = Button(root, text="3", padx=40, pady=20)
button_4 = Button(root, text="4", padx=40, pady=20)
button_5 = Button(root, text="5", padx=40, pady=20)
button_6 = Button(root, text="6", padx=40, pady=20)
button_7 = Button(root, text="7", padx=40, pady=20)
button_8 = Button(root, text="8", padx=40, pady=20)
button_9 = Button(root, text="9", padx=40, pady=20)

button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)

button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)

button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)



def myClick():
	hello = "Hello " + e.get()
	myLabel = Label(root, text=hello)
	myLabel.pack()

#myButton = Button(root, text="Enter Your Stock Quote", command=myClick)
#myButton.pack()



root.mainloop()