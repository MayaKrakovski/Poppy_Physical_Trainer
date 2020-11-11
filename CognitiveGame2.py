# -*- coding: utf-8 -*-
import Tkinter as tk
from PIL import Image, ImageTk
import Settings as s
import random
from Camera import Camera


class Screen(tk.Tk):
    def __init__(self):
        print("screen start")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(GameTwoStart)
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

class GameTwoStart(tk.Frame):
    def __init__(self, master):
        #TODO - RECORD GAME 2 INSTURCTIONS
        s.str_to_say = "game 2 instructions"
        tk.Frame.__init__(self, master)
        image1 = Image.open('Pictures//instructionGame2.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        image2 = Image.open('Pictures//continuebutton.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2 = tk.Button(self.background_label, image=self.photo_image2, command= lambda: self.on_click(master))
        button2.pack()
        button2.place(height=200, width=200, x=400, y=400)

    def on_click(self, master):
        self.background_label.destroy()
        s.screen.switch_frame(Game2PageOne)

class Game2PageOne(tk.Frame):
    def __init__(self, master):
        s.cogGameCount = s.cogGameCount + 1
        tk.Frame.__init__(self, master)
        image1 = Image.open('Pictures//background.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()

        self.labels=[]
        square_length=5
        corx = 600
        cory = 150

        for i in range(square_length*square_length):
            label = tk.Label(font=("Ariel", 40), bg="gray")
            label.pack()
            label.place(height=60, width=60, x=corx, y=cory)
            corx = corx - 70
            if corx <= 250:
                cory = cory + 70
                corx = 600
            self.labels.append(label)

        global light_tiles_num
        light_tiles_num=7
        global light_tiles
        light_tiles=[]
        while len(light_tiles) != light_tiles_num:
            number = random.randint(0,square_length*square_length-1)
            if number not in light_tiles:
                light_tiles.append(number)
                self.after(500, self.changeColor1, number)
        print (light_tiles)

        self.after(4000,lambda: self.on_click(master))

    def changeColor1(self, number):
        self.labels[number].configure(background="blue")

    def on_click(self, master):
        self.background_label.destroy()
        s.screen.switch_frame(Game2PageTwo)

class Game2PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//background.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        self.background_label = tk.Label(image=self.photo_image)
        self.background_label.pack()

        self.buttons=[]
        square_length=5
        corx = 600
        cory = 150

        for i in range(square_length*square_length):
            button = tk.Button(self.background_label, bg="gray", command = lambda button_number = i: self.on_click(button_number))
            button.pack()
            button.place(height=60, width=60, x=corx, y=cory)
            corx = corx - 70
            if corx <= 250:
                cory = cory + 70
                corx = 600
            self.buttons.append(button)

        self.count = 0 # to count the number of tries, we will limit to 10
        self.count_successes = 0

    def on_click(self,i):
        if (i in light_tiles):
            self.buttons[i].configure(background="blue")
            self.count_successes = self.count_successes+1
            s.str_to_say = "correct"
        else:
            self.buttons[i].configure(text="X", fg="red",font=("Courier", 44))
        self.count = self.count + 1
        if (self.count_successes == light_tiles_num):
            self.finishGamePage(True)
        if (self.count==10):
            self.finishGamePage(False)

    def finishGamePage(self, success):
        if (success):
            s.screen.switch_frame(SuccessPage)
            print ("success")
        else:
            s.screen.switch_frame(WorngPage)
            print("didn't succeed")
        # time.sleep(5)
        s.ex_list.append(["cog_game2", success])
        s.cogGame = False

class SuccessPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//success.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()

class WorngPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//worng.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=0
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
    words_number = 4
    choosen_words = []
    words_order = []
    s.cogGameCount = 0
    s.camera = Camera()
    s.screen = Screen()
    # width=s.screen.winfo_screenwidth()
    # height=s.screen.winfo_screenheight()
    # window_size=str(width)+'x'+str(height)
    # s.screen.geometry(window_size)
    app = FullScreenApp(s.screen)
    image1 = Image.open('Pictures//icon.jpg')
    s.screen.tk.call('wm', 'iconphoto', s.screen._w, ImageTk.PhotoImage(image1))
    s.screen.mainloop()