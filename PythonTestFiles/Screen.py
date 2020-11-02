# -*- coding: utf-8 -*-
import Tkinter
from PIL import Image, ImageTk
import random


import Tkinter as tk
global choosen_words
global words_order
global words_number

class GamePageOne(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        image1 = Image.open('Pictures//background.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        background_label = tk.Label(image=self.photo_image1).pack()

        corx = 1100
        cory = 155
        words = ["כפית", "כדור", "אהבה", "ילד", "אדום", "טלפון", "מכונית", "חתול", "כלב"]
        while len(choosen_words) != words_number:
            word = random.choice(words)
            if word not in choosen_words:
                choosen_words.append(word)

        self.labels = []
        for i in range(words_number):
            label = tk.Label(background_label, text = choosen_words[i], font=("Ariel", 40), bg="#F3FCFB")
            label.pack()
            label.place(height=120, width=150, x=corx, y=cory)
            corx = corx - 200
            self.labels.append(label)

        words_order = []
        i = 0
        while len(words_order) != words_number:
            number = random.randint(0,words_number-1)
            if number not in words_order:
                words_order.append(number)
                self.after(3000*i+1000, self.changeColor1, number)
                i = i + 1
        print (words_order)

        button2 = tk.Button(background_label, text = "המשך", font=("Ariel", 40), bg="red", command=self.on_click_right)
        button2.pack()
        button2.place(height=100, width=150, x=290, y=0)

    def changeColor1(self, number):
        self.labels[number].configure(background="yellow")
        self.after(3000, self.changeColor2, number)

    def changeColor2(self, number):
        self.labels[number].configure(bg="#F3FCFB")

    def on_click_right(self):
        self.switch_frame(GamePageTwo)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class GamePageTwo(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        image1 = Image.open('Pictures//background.jpg')
        self.photo_image1 = ImageTk.PhotoImage(image1)
        background_label = tk.Label(image=self.photo_image1).pack()
        corx = 1100
        cory = 155

        self.labels = []
        for i in range(words_number):
            label = tk.Button(background_label, text = choosen_words[i], font=("Ariel", 40), bg="#F3FCFB")
            label.pack()
            label.place(height=120, width=150, x=corx, y=cory)
            corx = corx - 200
            self.labels.append(label)



if __name__ == "__main__":
    words_number = 5
    choosen_words = []
    root = tk.Tk()
    Example1(root).pack(fill="both", expand=True)
    root.mainloop()