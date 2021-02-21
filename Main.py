import time
import random
from Poppy import Poppy #
from Camera import Camera
from tts import TTS
import Settings as s #Global settings variables
from GUI2 import Screen, FullScreenApp
from PIL import Image, ImageTk
import Excel as excel



if __name__ == '__main__':
    # Settings for exercises
    language = 'Hebrew'
    gender = 'Male'
    s.with_cog = False # Depnding on experiment scenario
    s.audio_path = 'audio files/' + language + '/' + gender + '/'

    s.exercies_amount = 6

    s.waved = False
    s.finish_workout = False
    s.rep = 8  # Number of repetitions for exercises
    s.req_exercise = ""
    s.str_to_say = ""
    s.clickedTryAgain = False
    s.cogGame = False
    # s.cogGameCount = 0
    excel.create_workbook()

    s.robot = Poppy()
    s.camera = Camera()
    s.tts = TTS()

    s.tts.start()
    s.robot.start()
    s.camera.start()

    s.screen = Screen()
    image1 = Image.open('Pictures//icon.jpg')
    s.screen.tk.call('wm', 'iconphoto', s.screen._w, ImageTk.PhotoImage(image1))
    app = FullScreenApp(s.screen)
    s.screen.mainloop()