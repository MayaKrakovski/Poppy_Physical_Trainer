# -*- coding: utf-8 -*-
import time
import Tkinter as tk
from PIL import Image, ImageTk
import Settings as s
import random

class Screen(tk.Tk):
    def __init__(self):
        print("screen start")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(HelloPage)
        self["bg"]="#F3FCFB"

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            if hasattr(self._frame, 'background_label'):
                self._frame.background_label.destroy()
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    # def switchFromtryAgaintoBlank(self):
    #     self._frame.background_label.destroy()
    #     s.screen.switch_frame(BlankPage)

    def quit(self):
        self.destroy()

class HelloPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//Hello.jpg')
        self.photo_image = ImageTk.PhotoImage(image) #self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image = self.photo_image).pack()

class ExercisePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//exercise.jpg')
        self.photo_image = ImageTk.PhotoImage(image) #self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image = self.photo_image).pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image1 = Image.open('Pictures//Start.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open('Pictures//StartButton.jpg')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2= tk.Button(image=self.photo_image2, command=self.on_click)
        button2.pack()
        button2.place(height=480, width=480, x=265, y=100)

    def on_click(self):
        print("image clicked")
        s.waved = True

class TryAgainPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image1 = Image.open('Pictures//tryagain.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        image2 = Image.open('Pictures//tryagainright2.jpg')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2= tk.Button(image=self.photo_image2, command=self.on_click_right)
        button2.pack()
        button2.place(height=350, width=350, x=535, y=155)

        image3 = Image.open('Pictures//tryagainleft2.jpg')
        self.photo_image3 = ImageTk.PhotoImage(image3)
        button2= tk.Button(image=self.photo_image3, command=self.on_click_left)
        button2.pack()
        button2.place(height=350, width=360, x=135, y=155)


    def on_click_right(self):
        print("image clicked")
        s.waved = True
        s.screen.switch_frame(BlankPage)

    def on_click_left(self):
        print("image clicked")
        s.clickedTryAgain=True
        s.screen.switch_frame(BlankPage)

class BlankPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//Background.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()

class VeryGoodPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//verygood.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()

class ExcellentPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//excellent.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()

class WellDonePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//welldone.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()

class GoodbyePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//Goodbye.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()

class OnePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//1.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom


if __name__ == "__main__":
    s.screen = Screen()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()