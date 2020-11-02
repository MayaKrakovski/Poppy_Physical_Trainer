import threading
import Settings as s
import winsound
from pygame import mixer
import time

class TTS(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print ("tts init")

    def run(self):
        while (not s.finish_workout):
            if (s.str_to_say!=""):
                self.say_no_wait(s.str_to_say)
                print("tts says: ", s.str_to_say)
                s.str_to_say = ""
        print ("tts done")

    def say(self, str_to_say):
        if (str_to_say != ""):
            winsound.PlaySound(s.audio_path+str_to_say+'.wav', winsound.SND_FILENAME)

    def say_no_wait(self, str_to_say):
        '''
        str_to_say = the name of the file
        This function make the robot say whatever there is in the file - play the audio (paralelly)
        :return: audio
        '''
        mixer.init()
        mixer.music.load(s.audio_path+str_to_say+'.wav')
        mixer.music.play()

if __name__ == '__main__':
    language = 'Hebrew'
    gender = 'Female'
    s.audio_path = 'audio files/' + language + '/' + gender + '/'

    tts = TTS()
    tts.say('raise arms forward')
    time.sleep(5)
