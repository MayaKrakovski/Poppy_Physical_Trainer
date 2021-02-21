# -*- coding: utf-8 -*-
import Tkinter as tk
from PIL import Image, ImageTk
import PIL.Image
import Settings as s
import random
import time
import copy
from Camera import Camera
from tts import TTS


class Screen(tk.Tk):
    def __init__(self):
        print("screen start")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(GameOneStart)
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

class GameOneStart(tk.Frame):
    def __init__(self, master):
        s.str_to_say = "game 1 instructions"
        tk.Frame.__init__(self, master)
        image1 = Image.open('Pictures//instructionGame1.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        image2 = Image.open('Pictures//continuebutton.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2 = tk.Button(image=self.photo_image2, command= lambda: self.on_click(master))
        button2.pack()
        button2.place(height=200, width=200, x=400, y=400)

        s.words_number = 4

    def on_click(self, master):
        self.background_label.destroy()
        s.screen.switch_frame(GamePageOne)

class GamePageOne(tk.Frame):
    def __init__(self, master):
        s.cogGameCount = s.cogGameCount + 1
        tk.Frame.__init__(self, master)
        image1 = Image.open('Pictures//background.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()


        s.choosen_words = []
        s.words_order = []
        corx = 750
        cory = 120

        words = ["רמז", "מים", "תפוח", "בית", "פרח", "נייר", "מחשב", "בקבוק", "מחשבון", "בקבוק", "עפרון", "קלמר", "צבע", "שפה", "מאמן", "אור", "הופעה", "עיתון", "אינטרנט", "ספר", "ספורט"]
        while len(s.choosen_words) != s.words_number:
            word = random.choice(words)
            if word not in s.choosen_words:
                s.choosen_words.append(word)

        self.labels = []
        for i in range(s.words_number):
            label = tk.Label(text = s.choosen_words[i], font=("Ariel", 40), bg="#F3FCFB")
            label.pack()
            label.place(height=120, width=150, x=corx, y=cory)
            corx = corx - 200
            if corx < 150:
                cory = cory + 150
                corx = 750
            self.labels.append(label)

        i = 0
        while len(s.words_order) != s.words_number:
            number = random.randint(0,s.words_number-1)
            if number not in s.words_order:
                s.words_order.append(number)
                self.after(1500*i+1000, self.changeColor1, number)
                i = i + 1
        print (s.words_order)

        # self.button2 = tk.Button(text = "המשך", font=("Ariel", 40), bg="red", command= lambda: self.on_click(master))
        # self.button2.pack()
        # self.button2.place(height=100, width=150, x=290, y=0)

        image2 = Image.open('Pictures//continuebutton.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        button2 = tk.Button(image=self.photo_image2, command= lambda: self.on_click(master))
        button2.pack()
        button2.place(height=200, width=200, x=400, y=400)

    def changeColor1(self, number):
        self.labels[number].configure(background="yellow")
        self.after(1500, self.changeColor2, number)

    def changeColor2(self, number):
        self.labels[number].configure(bg="#F3FCFB")

    def on_click(self,master):
        self.background_label.destroy()
        s.screen.switch_frame(GamePageTwo)

class GamePageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//background.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        self.background_label = tk.Label(image=self.photo_image)
        self.background_label.pack()
        corx = 750
        cory = 155

        new_words_order = copy.deepcopy(s.choosen_words)
        random.shuffle(new_words_order)

        self.count = 0
        self.labels = []

        for i in range(s.words_number):

            label = tk.Button(text = new_words_order[i], font=("Ariel", 40), bg="#F3FCFB", command =lambda but2=i,button_number= s.choosen_words.index(new_words_order[i]): self.on_click(but2,button_number))
            label.pack()
            label.place(height=120, width=150, x=corx, y=cory)

            corx = corx - 200
            if corx < 150:
                cory = cory + 150
                corx = 750
            self.labels.append(label)

    def changeColor2(self, number):
        self.labels[number].configure(bg="#F3FCFB")

    def on_click(self, but2,button_number):
        print (button_number)

        if (s.words_order[self.count] == button_number):
            self.labels[self.count]
            self.labels[but2].configure(bg="yellow")
            self.count = self.count + 1
            print ("good")
            self.after(1500,self.changeColor2,but2)
            s.str_to_say ="correct"
            if (self.count == s.words_number):
                self.finishGamePage(True)
        else:
            self.labels[but2].configure(bg="red")
            s.str_to_say = "bad"
            self.after(1500, self.changeColor2, but2)
            self.update()
            print ("bad")
            self.finishGamePage(False)

    def finishGamePage(self, success):
        if (success):
            s.screen.switch_frame(SuccessPage)
            s.words_number += 1
            print ("success")
        else:
            s.screen.switch_frame(WorngPage)
            s.words_number -= 1
            print("didn't succeed")
        s.ex_list.append(["cog_game1", success])

class SuccessPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//success.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        self.after(3000, self.last)

    def last(self):
        if s.cogGameCount >= 3:
            s.cogGame = False
        else:
            s.screen.switch_frame(GamePageOne)


class WorngPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//worng.jpg')
        self.photo_image = ImageTk.PhotoImage(image)
        tk.Label(self, image=self.photo_image).pack()
        self.after(3000, self.last)

    def last(self):
        if s.cogGameCount >= 3:
            s.cogGame = False
        else:
            s.screen.switch_frame(GamePageOne)


class HelloPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('Pictures//Hello.jpg')
        self.photo_image = ImageTk.PhotoImage(image) #self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image = self.photo_image).pack()

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
    words_number = 4
    choosen_words = []
    words_order = []
    s.ex_list = []
    s.cogGameCount = 0
    s.finish_workout = False
    s.camera = Camera()
    s.screen = Screen()
    language = 'Hebrew'
    gender = 'Female'
    s.audio_path = 'audio files/' + language + '/' + gender + '/'
    s.tts = TTS()
    s.tts.start()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()