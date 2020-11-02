import sys, os, time
import threading


class Realsense (threading.Thread) :

    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        #Need to change for Nuitrack!
        os.system("C:\\Users\\mayak\\Cubemos-Samples\\build\\cpp\\realsense\\Debug\\cpp-realsense.exe")
    def stop(self):
        #Need to change for Nuitrack!
        os.system("taskkill /f /im  cpp-realsense.exe")

if __name__ == '__main__':
    r = Realsense()
    r.run()
