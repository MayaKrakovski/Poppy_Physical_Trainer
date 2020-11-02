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
from datetime import date,datetime
from numpy import savetxt


class Screen(tk.Tk):
    def __init__(self):
        print("screen start")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(GameThreeStart)
        self["bg"] = "#F3FCFB"

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            if hasattr(self._frame, 'background_label'):
                self._frame.background_label.destroy()
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class GameThreeStart(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #TODO - RECORD GAME 3 INSTURCTIONS
        s.str_to_say = "game 3 instructions"
        image1 = Image.open('Pictures//instructionGame3.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.label = tk.Label(image=self.photo_image1)
        self.label.pack()
        image2 = Image.open('Pictures//continuebutton.png')
        self.photo_image2 = ImageTk.PhotoImage(image2)
        self.button = tk.Button(image=self.photo_image2, command=lambda: self.onclick(master))
        self.button.pack()
        self.button.place(height=200, width=200, x=650, y=350)

    def onclick(self,master):
        self.label.destroy()
        self.button.destroy()
        s.screen.switch_frame(Game3PageOne)


class Game3PageOne(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        self.math_generate()

    def math_generate(self):
        maths_functions = [self.additions]
        self.first = random.randint(1, 9)
        self.second = random.randint(1, 9)
        temp=0
        if (self.first<self.second):
            temp=self.first
            self.first=self.second
            self.second=temp
        print(self.first)
        print(self.second)
        fun_choice = random.choice(maths_functions)
        print(fun_choice)
        fun_choice()

    def additions(self):
        ans_right = self.first + self.second
        answer = [ans_right, random.randint(1, 20), random.randint(1, 20), random.randint(1, 20)]
        image1 = Image.open('Pictures/cognitive3_background.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        label = tk.Label(text=str(self.first) + "  +  " + str(self.second)+ " = ? ", font=("Ariel", 40), bg="white")
        label.pack()
        label.place(height=100, width=300, x=550, y=250)
        corx = 400
        cory = 400
        random.shuffle(answer)
        self.button2=[]
        for i in range(len(answer)):
            button = tk.Button(text=str(answer[i]), font=("Ariel", 36), bg="white",
                               command=lambda ans_right=ans_right, i=i, current_number=answer[i]: self.check_respons(ans_right, i,
                                                                                                    current_number))
            button.pack()
            button.place(height=100, width=100, x=corx, y=cory)
            print(corx, cory)
            if corx == 1000:
                corx-=200
                cory+=200
            else:
                corx += 150
            self.button2.append(button)
    def changeColor2(self, number):
        self.button2[number].configure(bg="#F3FCFB")

    def check_respons(self, ans_right, i, current_number):
        if (ans_right == current_number):
            print("success")
            print(self.button2)
            self.button2[i].configure(bg="yellow")
            self.after(6000,self.changeColor2,i)
            self.update()


            print("well done")
            s.str_to_say = "correct"
            time.sleep(1)
            self.finishGamePage(True)
            # self.success()
        else:
            self.button2[i].configure(bg="red")
            self.after(6000, self.changeColor2, i)
            self.update()
            s.str_to_say = "GAME OVER"
            time.sleep(1)
            self.finishGamePage(False)
            print("failure")

    def substractions(self):

        ans_right = self.first - self.second


        print(ans_right)
        answer = [ans_right, random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)]
        image1 = Image.open('Pictures//cognitive3_background.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        label = tk.Label(text=str(self.first) + "  -  " + str(self.second)+" = ? ", font=("Ariel", 40), bg="white")
        label.pack()
        label.place(height=100, width=300, x=280, y=250)
        corx = 150
        cory = 400
        random.shuffle(answer)
        self.button2 = []
        for i in range(len(answer)):

            button = tk.Button(text=str(answer[i]), font=("Ariel", 36), bg="white",
                               command=lambda ans_right=ans_right, i=i, current_number=answer[i]: self.check_respons(ans_right, i,
                                                                                                    current_number))
            button.pack()
            button.place(height=100, width=100, x=corx, y=cory)
            print(corx, cory)
            if corx == 1000:
                corx -= 200
                cory += 200
            else:
                corx += 150
            self.button2.append(button)


    def multiplications(self):
        self.first = random.randint(1, 5)
        self.second = random.randint(1, 6)
        ans_right = self.first * self.second



        answer = [ans_right, random.randint(1, 30), random.randint(1, 30), random.randint(1, 30)]
        image1 = Image.open('Pictures//cognitive3_background.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        self.background_label = tk.Label(image=self.photo_image1)
        self.background_label.pack()
        label = tk.Label(text=str(self.first) + "  X  " + str(self.second)+ " = ? ", font=("Ariel", 40), bg="white")
        label.pack()
        label.place(height=100, width=300, x=280, y=250)
        corx = 150
        cory = 400
        random.shuffle(answer)
        self.button2 = []
        for i in range(len(answer)):

            button = tk.Button(text=str(answer[i]), font=("Ariel", 32), bg="white",
                               command=lambda ans_right=ans_right, i=i, current_number=answer[i]: self.check_respons(ans_right, i,
                                                                                                    current_number))
            button.pack()
            button.place(height=100, width=100, x=corx, y=cory)
            print(corx,cory)
            if corx == 1000:
                corx -= 200
                cory += 200
            else:
                corx += 150
            self.button2.append(button)
    def finishGamePage(self, success):
        now=datetime.now()
        if (success):
            s.screen.switch_frame(SuccessPage)
            # dt_t = str(date.today())
            # td_t = str(now.strftime("%H:%M:%S"))
            # mylist = [dt_t, td_t, 'success']
            # with open("C:/Users/Administrator/PycharmProjects/greatoded/oded_gr8_cog.csv", "ab") as f:
            #     f.write(b"\t")
            #     savetxt(f, mylist, fmt='%s')
            # mylst=["cognative mission maths- success"]
            # with open("C:/Users/Administrator/PycharmProjects/greatoded/data_shik.csv", "ab") as f:
            #     f.write(b"\t")
            #     savetxt(f, mylst, fmt='%s')
            print ("success")
        else:
            s.screen.switch_frame(SuccessPage)
            # dt_t = str(date.today())
            # td_t = str(now.strftime("%H:%M:%S"))
            # mylist = [dt_t, td_t, 'Failure']
            # with open("C:/Users/Administrator/PycharmProjects/greatoded/oded_gr8_cog.csv", "ab") as f:
            #     f.write(b"\t")
            #     savetxt(f, mylist, fmt='%s')
            # mylst = ["cognative mission maths- Failure"]
            # with open("C:/Users/Administrator/PycharmProjects/greatoded/data_shik.csv", "ab") as f:
            #     f.write(b"\t")
            #     savetxt(f, mylst, fmt='%s')
            # s.screen.switch_frame(WorngPage)
            print("didn't succeed")
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
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom


if __name__ == "__main__":

    s.count=0
    s.cogGameCount = 0
    s.finish_workout = False
    s.camera = Camera()
    s.screen = Screen()
    language = 'Hebrew'
    gender = 'Male'
    audiopath = R'C:\Users\Administrator\PycharmProjects\greatoded\audio files'
    s.audio_path = audiopath + language + '/' + gender + '/'
    s.tts = TTS()
    s.tts.start()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()